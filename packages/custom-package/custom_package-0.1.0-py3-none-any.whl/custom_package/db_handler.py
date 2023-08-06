from custom_package.db_config import DBConfig
from custom_package.db_binding import PostgresHandler


handler = PostgresHandler(
    DBConfig.DB_HOST,
    DBConfig.DB_USER,
    DBConfig.DB_NAME,
    DBConfig.DB_PASSWORD,
    DBConfig.DB_PORT,
    DBConfig.DB_POOLSIZE,
)


def register_models():
    handler.initialize_db()
    from custom_package.models.customers import Customers
    handler.Base.metadata.create_all(bind=handler.engine)