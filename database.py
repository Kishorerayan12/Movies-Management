from typing import Any, Generator

# from sqlmodel import SQLModel, Session, create_engine
from sqlmodel import SQLModel, Session, create_engine



def get_url() -> str:
    """ Get database connection URL as a str. """
    return "mysql+mysqlconnector://root:admin123@127.0.0.1/netflix"


def get_session() -> Generator[Session, Any, None]:
    """ :return: A Generator with a database session. This will close automatically. """
    with Session(engine) as db:
        yield db


def initialize():
    """ Initializes the database with all models if the table(s) do not exist. """
    from app import tables
    print('database.py: Initializing: %s', tables.__name__)

    SQLModel.metadata.create_all(engine)


def dispose():
    engine.dispose()


engine = create_engine(get_url())
print("66666666", engine)
if __name__ == "__main__":
    initialize()
    dispose()
