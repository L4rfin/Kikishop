import sqlalchemy
from database.database_connection import Base

class Statistic(Base):

    __tablename__ = "statistic"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, autoincrement=True, primary_key=True)
    amount_of_item = sqlalchemy.Column(sqlalchemy.INTEGER, nullable=False)
    visits = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False)

