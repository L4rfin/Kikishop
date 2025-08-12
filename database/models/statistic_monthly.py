import sqlalchemy
from database.database_connection import Base

class StatisticMonth(Base):

    __tablename__ = "statistic_monthly"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, autoincrement=True, primary_key=True)
    visits = sqlalchemy.Column(sqlalchemy.BIGINT)

    # new orders:
    order_new = sqlalchemy.Column(sqlalchemy.INTEGER)
    amount_of_item_in_new_order = sqlalchemy.Column(sqlalchemy.BIGINT)
    amount_of_money_in_new_order = sqlalchemy.Column(sqlalchemy.BIGINT)

    # processed order
    order_processed = sqlalchemy.Column(sqlalchemy.INTEGER)
    amount_of_item_in_processed_order = sqlalchemy.Column(sqlalchemy.BIGINT)
    amount_of_money_in_processed_order = sqlalchemy.Column(sqlalchemy.INTEGER)

    # finish order
    order_finish = sqlalchemy.Column(sqlalchemy.INTEGER)
    amount_of_item_sent = sqlalchemy.Column(sqlalchemy.INTEGER)
    value_total = sqlalchemy.Column(sqlalchemy.BIGINT)

    # drop order
    order_drop = sqlalchemy.Column(sqlalchemy.BIGINT)
    drop_new_order = sqlalchemy.Column(sqlalchemy.BIGINT)
    drop_processed_order = sqlalchemy.Column(sqlalchemy.BIGINT)
    drop_finsh_order = sqlalchemy.Column(sqlalchemy.BIGINT)

    data = sqlalchemy.Column(sqlalchemy.DATE,nullable=False)
