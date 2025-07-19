import sqlalchemy
from database.database_connection import Base

class Order(Base):

    __tablename__ = "order"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, autoincrement=True, primary_key=True)
    items = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=False)
    city = sqlalchemy.Column(sqlalchemy.SMALLINT, nullable=False)
    street = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    postal_code = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    building_number = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    status = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    order_data = sqlalchemy.Column(sqlalchemy.DATE,nullable=False)