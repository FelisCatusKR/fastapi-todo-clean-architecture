from contextlib import contextmanager, AbstractContextManager
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from .model import Todo


class InMemoryDatabase:
    def __init__(self):
        self._list = []
        self._counter = 0

    def add_item(self, todo: Todo) -> Todo:
        self._counter += 1
        new_todo = Todo(todo_id=self._counter, title=todo.title, is_completed=todo.is_completed)
        self._list.append(new_todo)
        return new_todo

    def get_item_by_id(self, todo_id: int) -> Todo | None:
        return next((todo for todo in self._list if todo.todo_id == todo_id), None)

    def get_all_items(self) -> list[Todo]:
        return [todo for todo in self._list]

    def remove_item(self, todo_id: int):
        pass


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
