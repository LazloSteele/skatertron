import contextlib

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from typing import Any
from config import settings
from contextlib import contextmanager
Base = declarative_base()


class SessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = None):
        if engine_kwargs is None:
            engine_kwargs = {}

        self._engine = create_engine(host, **engine_kwargs)
        self._sessionmaker = sessionmaker(bind=self.engine, expire_on_commit=False)

    @property
    def engine(self):
        return self._engine

    def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    def connect(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                connection.rollback()
                raise Exception

    @contextmanager
    def session(self):
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise Exception
        finally:
            session.close()


session_manager = SessionManager(
    settings.database_url,
    {"echo": settings.echo_sql}
)


def get_db_session():
    with session_manager.session() as session:
        yield session
