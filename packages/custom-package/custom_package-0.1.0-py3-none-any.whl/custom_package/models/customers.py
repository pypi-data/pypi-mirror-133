from sqlalchemy import (
    Column,
    Integer,
    String
)
from custom_package.db_handler import handler


class Customers(handler.Base):

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    description_change = Column(String)

    def __repr__(self):
        return self.first_name + self.last_name
