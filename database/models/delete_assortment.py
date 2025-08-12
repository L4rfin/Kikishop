import sqlalchemy
from database.database_connection import Base

class DeleteAssortment(Base):

    __tablename__ = "delete_assortment"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, autoincrement=True, primary_key=True)
    item_id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False)
    cause = sqlalchemy.Column(sqlalchemy.VARCHAR(50), nullable=False)
    description_of_item = sqlalchemy.Column(sqlalchemy.VARCHAR(50), nullable=False)