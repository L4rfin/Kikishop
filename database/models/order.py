import sqlalchemy
from database.database_connection import Base


class Order(Base):
    __tablename__ = "client_order"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, autoincrement=True, primary_key=True)

    # general order info
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    items = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    items_amount = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    order_data = sqlalchemy.Column(sqlalchemy.DATE, nullable=False)

    # customer address
    city = sqlalchemy.Column(sqlalchemy.SMALLINT, nullable=False)
    street = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    postal_code = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    cuntry = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    building_number = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)

    # contact address
    email = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
