import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):

    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                              nullable=True)
    members = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("jobs.collaborators"),
                                nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    creator = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user = orm.relation("User")
    jobs = orm.relation("Jobs")
