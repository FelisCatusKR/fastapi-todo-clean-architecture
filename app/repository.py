import abc
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import InMemoryDatabase
from .model import Todo


class AbstractTodoRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, todo: Todo) -> Todo:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, todo_id: UUID) -> Todo | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> list[Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, todo: Todo) -> bool:
        raise NotImplementedError


class InMemoryTodoRepository(AbstractTodoRepository):
    def __init__(self, db: InMemoryDatabase):
        self._db = db

    def add(self, todo: Todo) -> Todo:
        return self._db.add_item(todo)

    def get_by_id(self, todo_id: UUID) -> Todo | None:
        return self._db.get_item_by_id(todo_id)

    def get_all(self) -> list[Todo]:
        return self._db.get_all_items()

    def delete(self, todo: Todo) -> bool:
        return self._db.remove_item(todo)


class SqlalchemyTodoRepository(AbstractTodoRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, todo: Todo) -> Todo:
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def get_by_id(self, todo_id: UUID) -> Todo | None:
        query_result = self.session.scalars(select(Todo).filter_by(todo_id).limit(1))
        return query_result.one_or_none()

    def get_all(self) -> list[Todo]:
        query_result = self.session.scalars(select(Todo))
        return query_result.all()

    def delete(self, todo: Todo):
        self.session.delete(todo)
        self.session.commit()
