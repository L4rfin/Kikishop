import sqlalchemy
from database.database_connection import Base

class Assortment(Base):

    __tablename__ = "assortment"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, autoincrement=True, primary_key=True)

    #general info
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(40), nullable=False)
    img = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=False)
    amount = sqlalchemy.Column(sqlalchemy.SMALLINT, nullable=False)
    amount_sold = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False)
    renewable = sqlalchemy.Column(sqlalchemy.VARCHAR(40), nullable=False)
    drop_data = sqlalchemy.Column(sqlalchemy.DATE,nullable=False)

    #item tags
    type = sqlalchemy.Column(sqlalchemy.VARCHAR(40), nullable=False)
    variant = sqlalchemy.Column(sqlalchemy.VARCHAR(40), nullable=False)
    tags = sqlalchemy.Column(sqlalchemy.VARCHAR(40), nullable=False)
    feature = sqlalchemy.Column(sqlalchemy.VARCHAR(40), nullable=False)
    work_source = sqlalchemy.Column(sqlalchemy.VARCHAR(40), nullable=False)
    material = sqlalchemy.Column(sqlalchemy.VARCHAR(40), nullable=False)
