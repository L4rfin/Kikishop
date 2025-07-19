import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://shopUser:R7KQAM5pf32EVAHNEnSF@127.0.0.1:3306/kikshop")
Base = declarative_base()