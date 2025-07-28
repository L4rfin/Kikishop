import sqlalchemy
from database.database_connection import Base

class Order(Base):

    __tablename__ = "client_order"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    items = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=False)
    street = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    postal_code = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    city = sqlalchemy.Column(sqlalchemy.SMALLINT, nullable=False)
    cuntry = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    building_number = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    status = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    order_data = sqlalchemy.Column(sqlalchemy.DATE,nullable=False)