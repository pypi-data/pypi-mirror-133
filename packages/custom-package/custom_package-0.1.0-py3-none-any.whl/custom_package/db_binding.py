from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    scoped_session,
    sessionmaker
)
from sqlalchemy_utils import database_exists, create_database


class PostgresHandler:

    def __init__(self,
                host,
                user,
                db_name,
                password,
                port,
                pool_size
                ):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db_name = db_name
        self.pool_size = pool_size
        self.__validate_credentials()
        self.url = self.get_connection_string()
        # pylint: disable=C0103
        # note: Ignoring C0103: Attribute name as it's a modeling class
        self.Base, self.engine = self.create_engine()

    def __validate_credentials(self):
        if not self.host:
            raise Exception("Host is not specified")
        if not self.user:
            raise Exception("User is not specified")
        if not self.password:
            raise Exception("Password is not specified")
        if not self.port:
            raise Exception("Port is not specified")
        if not self.db_name:
            raise Exception("Db name is not specified")

    def get_connection_string(self):
        url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        return url

    def create_engine(self):
        engine = create_engine(
            self.url, pool_size=self.pool_size, pool_pre_ping=True, pool_recycle=300, echo=False,
            isolation_level="READ UNCOMMITTED")
        db_session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
        base = declarative_base(bind=engine)
        base.query = db_session.query_property()
        return base, engine

    def initialize_db(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        else:
            # Connect the database if exists.
            self.engine.connect()
