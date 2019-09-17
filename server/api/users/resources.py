from flask_restful import Resource, current_app, request
from schematics.exceptions import DataError
from dateutil.parser import parse as date_parse

from server.models.dtos.user_dto import UserSearchQuery
from server.services.users.authentication_service import token_auth, tm
from server.services.users.user_service import UserService, NotFound


class UsersRestAPI(Resource):
    @tm.pm_only(False)
    @token_auth.login_required
    def get(self, userid):
        """
        Gets user information by id
        ---
        tags:
          - users
        produces:
          - application/json
        parameters:
            - in: header
              name: Authorization
              description: Base64 encoded sesesion token
              required: true
              type: string
              default: Token sessionTokenHere==
            - name: userid
              in: path
              description: The users user id
              required: true
              type: integer
              default: 1
        responses:
            200:
                description: User found
            404:
                description: User not found
            500:
                description: Internal Server Error
        """
        try:
            user_dto = UserService.get_user_dto_by_id(userid)
            return user_dto.to_primitive(), 200
        except NotFound:
            return {"Error": "User not found"}, 404
        except Exception as e:
            error_msg = f"Userid GET - unhandled error: {str(e)}"
            current_app.logger.critical(error_msg)
            return {"Error": "Unable to fetch user details"}, 500


class UsersAllAPI(Resource):
    def get(self):
        """
        Gets paged list of all usernames
        ---
        tags:
          - users
        produces:
          - application/json
        parameters:
            - in: query
              name: page
              description: Page of results user requested
              type: integer
            - in: query
              name: username
              description: Full or part username
              type: integer
            - in: query
              name: role
              description: Role of User, eg ADMIN, PROJECT_MANAGER
              type: string
            - in: query
              name: level
              description: Level of User, eg BEGINNER
              type: string
        responses:
            200:
                description: Users found
            500:
                description: Internal Server Error
        """
        try:
            query = UserSearchQuery()
            query.page = (
                int(request.args.get("page")) if request.args.get("page") else 1
            )
            query.username = request.args.get("username")
            query.mapping_level = request.args.get("level")
            query.role = request.args.get("role")
            query.validate()
        except DataError as e:
            current_app.logger.error(f"Error validating request: {str(e)}")
            return {"Error": "Unable to fetch user list"}, 400

        try:
            users_dto = UserService.get_all_users(query)
            return users_dto.to_primitive(), 200
        except Exception as e:
            error_msg = f"User GET - unhandled error: {str(e)}"
            current_app.logger.critical(error_msg)
            return {"Error": "Unable to fetch user list"}, 500


class UsersQueriesUsernameAPI(Resource):
    @tm.pm_only(False)
    @token_auth.login_required
    def get(self, username):
        """
        Gets user information
        ---
        tags:
          - users
        produces:
          - application/json
        parameters:
            - in: header
              name: Authorization
              description: Base64 encoded session token
              required: true
              type: string
              default: Token sessionTokenHere==
            - name: username
              in: path
              description: The users username
              required: true
              type: string
              default: Thinkwhere
        responses:
            200:
                description: User found
            404:
                description: User not found
            500:
                description: Internal Server Error
        """
        try:
            user_dto = UserService.get_user_dto_by_username(
                username, tm.authenticated_user_id
            )
            return user_dto.to_primitive(), 200
        except NotFound:
            return {"Error": "User not found"}, 404
        except Exception as e:
            error_msg = f"User GET - unhandled error: {str(e)}"
            current_app.logger.critical(error_msg)
            return {"Error": "Unable to fetch user details"}, 500


class UsersQueriesUsernameFilterAPI(Resource):
    def get(self, username):
        """
        Gets paged lists of users matching username filter
        ---
        tags:
          - users
        produces:
          - application/json
        parameters:
            - name: username
              in: path
              description: Partial or full username
              type: string
              default: ab
            - in: query
              name: page
              description: Page of results user requested
              type: integer
            - in: query
              name: projectId
              description: Optional, promote project participants to head of results
              type: integer
        responses:
            200:
                description: Users found
            404:
                description: User not found
            500:
                description: Internal Server Error
        """
        try:
            page = int(request.args.get("page")) if request.args.get("page") else 1
            project_id = request.args.get("projectId", None, int)
            is_project_manager = request.args.get("isProjectManager", False) == "true"
            users_dto = UserService.filter_users(
                username, project_id, page, is_project_manager
            )
            return users_dto.to_primitive(), 200
        except NotFound:
            return {"Error": "User not found"}, 404
        except Exception as e:
            error_msg = f"User GET - unhandled error: {str(e)}"
            current_app.logger.critical(error_msg)
            return {"Error": "Unable to fetch matching users"}, 500


class UserTasksAPI(Resource):
    @token_auth.login_required
    def get(self):
        """
        Gets tasks users has interacted
        ---
        tags:
          - user
        produces:
          - application/json
        parameters:
            - in: header
              name: Authorization
              description: Base64 encoded session token
              required: true
              type: string
              default: Token sessionTokenHere==
            - in: query
              name: status
              description: Project Status filter
              required: false
              type: string
              default: null
            - in: query
              name: project_id
              description: Project id
              required: false
              type: integer
              default: null
            - in: query
              name: start_date
              description: Date to filter as minimum
              required: false
              type: string
              default: null
            - in: query
              name: end_date
              description: Date to filter as maximum
              required: false
              type: string
              default: null
            - in: query
              name: sort_by
              description: field to sort by, supported fields: action_date, -action_date
              required: false
              type: string
              default: null
        responses:
            200:
                description: Mapped projects found
            404:
                description: No mapped projects found
            500:
                description: Internal Server Error
        """
        try:
            status = request.args.get("status")
            project_id = int(request.args.get("project_id", 0))
            start_date = (
                date_parse(request.args.get("start_date"))
                if request.args.get("start_date")
                else None
            )
            end_date = (
                date_parse(request.args.get("end_date"))
                if request.args.get("end_date")
                else None
            )
            sort_by = request.args.get("sort_by")

            tasks = UserService.get_tasks_dto(
                tm.authenticated_user_id,
                project_id=project_id,
                status=status,
                start_date=start_date,
                end_date=end_date,
                sort_by=sort_by,
            )
            return tasks.to_primitive(), 200
        except NotFound:
            return {"Error": "User or tasks not found"}, 404
        except Exception as e:
            error_msg = f"User GET - unhandled error: {str(e)}"
            current_app.logger.critical(error_msg)
            return {"error": error_msg}, 500
