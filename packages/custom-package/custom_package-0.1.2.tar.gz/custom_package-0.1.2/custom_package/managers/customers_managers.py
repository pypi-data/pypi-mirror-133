from sqlalchemy.orm import Query


class CustomersManager(Query):

    def get_customer_data(self, **kwargs):
        return self.filter_by(**kwargs)

    def filter_data(self, first_name):
        return self.filter_by(first_name=first_name)

    def get_first(self):
        return self.first()
