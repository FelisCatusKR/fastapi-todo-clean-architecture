import abc
from typing import Callable

from sqlalchemy.orm import Session

from . import repository


class AbstractTodoUnitOfWork(abc.ABC):
    todos: repository.AbstractTodoRepository

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class InMemoryTodoUnitOfWork(AbstractTodoUnitOfWork):
    _set: set

    def __init__(self):
        self._set = set()

    def __enter__(self):
        self.todos = repository.InMemoryTodoRepository(self._set)
        return super().__enter__()

    def commit(self):
        pass

    def rollback(self):
        pass


class SqlalchemyTodoUnitOfWork(AbstractTodoUnitOfWork):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.todos = repository.SqlalchemyTodoRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):  # (4)
        self.session.commit()

    def rollback(self):  # (4)
        self.session.rollback()
