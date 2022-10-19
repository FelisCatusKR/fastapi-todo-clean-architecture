from uuid import UUID

from .dto import TodoCreateDto
from .model import Todo
from .repository import AbstractTodoRepository


class TodoService:
    def __init__(self, todo_repository: AbstractTodoRepository):
        self._repository = todo_repository

    def get_all(self) -> list[Todo]:
        return self._repository.get_all()

    def get_by_id(self, todo_id: UUID) -> Todo | None:
        return self._repository.get_by_id(todo_id)

    def create_todo(self, dto: TodoCreateDto) -> Todo:
        todo = Todo(title=dto.title, is_completed=dto.is_completed)
        return self._repository.add(todo)

    def delete_by_id(self, todo_id: UUID) -> bool:
        todo = self._repository.get_by_id(todo_id)
        self._repository.delete(todo)
        return True
