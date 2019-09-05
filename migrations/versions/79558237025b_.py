"""empty message

Revision ID: 79558237025b
Revises: e3282e2db2d7
Create Date: 2019-08-22 03:08:15.746392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "79558237025b"
down_revision = "e3282e2db2d7"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "campaign",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("logo", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "campaign_projects",
        sa.Column("campaign_id", sa.Integer(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaign.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
    )
    op.create_table(
        "campaign_organisations",
        sa.Column("campaign_id", sa.Integer(), nullable=True),
        sa.Column("organisation_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaign.id"]),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
    )
    op.drop_index(
        "idx_task_validation_mapper_status_composite",
        table_name="task_invalidation_history",
    )
    op.create_index(
        "idx_task_validation_mapper_status_composite",
        "task_invalidation_history",
        ["invalidator_id", "is_closed"],
        unique=False,
    )
    # ### end Alembic commands ###

    # Content migration: Migrate the campaigns tag in campaigns table
    campaigns = conn.execute("select campaigns from tags").fetchall()

    # This will be used to consolidate the data in tags table
    dictionaries = {"HOTOSM": {"HOTOSM", "HOT-OSM"}, "ABC": {"abc", "ABc"}}

    for campaign in campaigns:
        result = campaign[0]
        for campaign_key, campaign_values in dictionaries.items():
            if campaign[0] in campaign_values:
                result = campaign_key

        query = "insert into campaign(name) values('" + result + "')"
        op.execute(query)

    # Migrate the organisations tag in organisations table
    organisations = conn.execute("select organisations from tags").fetchall()

    # This will be used to consolidate the data in the tags table
    org_dictionaries = {"HOTOSM": {"HOTOSM", "HOT-OSM"}, "ABC": {"abc", "ABc"}}

    for org in organisations:
        result = org[0]
        for org_key, org_values in org_dictionaries.items():
            if result in org_values:
                result = org_key

        query = "insert into organisations(name) values ('" + result + "')"
        op.execute(query)


def downgrade():
    op.drop_table("campaign_projects")
    op.drop_table("campaign_organisations")
    op.drop_table("campaign")
