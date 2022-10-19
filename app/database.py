from contextlib import contextmanager, AbstractContextManager
from typing import Callable
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from .model import Todo


class InMemoryDatabase:
    _list: list[Todo]

    def __init__(self):
        self._list = []

    def add_item(self, todo: Todo) -> Todo:
        new_todo = Todo(title=todo.title, is_completed=todo.is_completed)
        self._list.append(new_todo)
        return new_todo

    def get_item_by_id(self, todo_id: UUID) -> Todo | None:
        return next((todo for todo in self._list if todo.todo_id == todo_id), None)

    def get_all_items(self) -> list[Todo]:
        return [todo for todo in self._list]

    def remove_item(self, todo: Todo):
        self._list = [item for item in self._list if item.todo_id != todo.todo_id]
        return True


class SqlalchemyDatabase:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
