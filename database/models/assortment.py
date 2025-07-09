import sqlalchemy
from database.database_connection import Base

class Assortment(Base):

    __tablename__ = "assortment"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    img = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=False)
    amount = sqlalchemy.Column(sqlalchemy.SMALLINT, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    genre = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    renewable = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    character_source = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    drop_data = sqlalchemy.Column(sqlalchemy.DATE,nullable=False)