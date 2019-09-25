import json

from server import db

from sqlalchemy import func

from server.models.dtos.interests_dto import (
    InterestsDTO,
    InterestrateDTO,
    InterestratesDTO,
)
from server.models.postgis.task import TaskHistory
from server.models.postgis.interests import Interest, projects_interests
from server.services.project_service import ProjectService
from server.services.users.user_service import UserService


class InterestService:
    @staticmethod
    def get_by_id(interest_id):
        interest = Interest.get_by_id(interest_id)
        return interest

    @staticmethod
    def create(interest_name):
        interest_model = Interest(name=interest_name)
        interest_model.create()
        return interest_model.as_dto()

    @staticmethod
    def update(interest_id, new_interest_dto):
        interest = InterestService.get_by_id(interest_id)
        interest.update(new_interest_dto)
        return interest.as_dto()

    @staticmethod
    def load_from_file(file):
        with open(file, "r") as f:
            data = json.load(f)

        for interest in data:
            interest_model = Interest(name=interest["name"])
            interest_model.create()

    @staticmethod
    def get_all_interests():
        interests = Interest.query.all()
        dto = InterestsDTO()
        dto.interests = [i.as_dto() for i in interests]

        return dto

    @staticmethod
    def delete(interest_id):
        interest = InterestService.get_by_id(interest_id)
        interest.delete()

    @staticmethod
    def create_or_update_project_interests(project_id, interests):
        project = ProjectService.get_project_by_id(project_id)
        project.create_or_update_interests(interests)

        # Return DTO.
        dto = InterestsDTO()
        dto.interests = [i.as_dto() for i in project.interests]

        return dto

    @staticmethod
    def create_or_update_user_interests(user_id, interests):
        user = UserService.get_user_by_id(user_id)
        user.create_or_update_interests(interests)

        # Return DTO.
        dto = InterestsDTO()
        dto.interests = [i.as_dto() for i in user.interests]

        return dto

    @staticmethod
    def compute_contributions_rate(user_id):
        # 1. Get all projects that user has contributed.
        stmt = (
            TaskHistory.query.with_entities(TaskHistory.project_id)
            .distinct()
            .filter(TaskHistory.user_id == user_id)
            .subquery()
        )

        res = (
            db.session.query(
                Interest.name,
                func.count(projects_interests.c.interest_id)
                / func.sum(func.count(projects_interests.c.interest_id)).over(),
            )
            .group_by(projects_interests.c.interest_id, Interest.name)
            .filter(projects_interests.c.project_id.in_(stmt))
            .join(Interest, Interest.id == projects_interests.c.interest_id)
        )

        rates = [InterestrateDTO({"name": r[0], "rate": r[1]}) for r in res.all()]
        results = InterestratesDTO()
        results.rates = rates

        return results
