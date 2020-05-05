import sqlalchemy
from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table('jobs_to_category', SqlAlchemyBase.metadata,
    sqlalchemy.Column('jobs', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('jobs.id')),
    sqlalchemy.Column('category', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('job_category.id'))
)


class CategoryJob(SqlAlchemyBase):

    __tablename__ = 'job_category'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
