import abc
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

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
    _set: set[Todo]

    def __init__(self, memory_set: set):
        self._set = memory_set

    def add(self, todo: Todo) -> Todo:
        new_todo = Todo(title=todo.title, is_completed=todo.is_completed)
        self._set.add(new_todo)
        return new_todo

    def get_by_id(self, todo_id: UUID) -> Todo | None:
        return next((todo for todo in self._set if todo.todo_id == todo_id), None)

    def get_all(self) -> list[Todo]:
        return [todo for todo in self._set]

    def delete(self, todo: Todo):
        self._set.remove(todo)
        return True


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
