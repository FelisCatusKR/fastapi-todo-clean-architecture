from uuid import UUID

from .dto import TodoCreateDto
from .model import Todo
from .uow import AbstractTodoUnitOfWork


class TodoService:
    def __init__(self, todo_uow: AbstractTodoUnitOfWork):
        self.uow = todo_uow

    def get_all(self) -> list[Todo]:
        with self.uow:
            return self.uow.todos.get_all()

    def get_by_id(self, todo_id: UUID) -> Todo | None:
        with self.uow:
            return self.uow.todos.get_by_id(todo_id)

    def create_todo(self, dto: TodoCreateDto) -> Todo:
        todo = Todo(title=dto.title, is_completed=dto.is_completed)
        with self.uow:
            return self.uow.todos.add(todo)

    def delete_by_id(self, todo_id: UUID) -> bool:
        with self.uow:
            todo = self.uow.todos.get_by_id(todo_id)
            return self.uow.todos.delete(todo)
