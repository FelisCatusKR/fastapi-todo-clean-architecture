from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from .container import Container
from .dto import TodoCreateDto
from .service import TodoService

router = APIRouter()


@router.get("/")
@inject
def get_all_todos(
    todo_service: TodoService = Depends(Provide[Container.todo_service])
):
    return todo_service.get_all()


@router.post("/")
@inject
def add_todo(
        todo_dto: TodoCreateDto,
        todo_service: TodoService = Depends(Provide[Container.todo_service])
):
    return todo_service.create_todo(todo_dto)


@router.get("/{todo_id}")
@inject
def get_todo_by_id(
        todo_id: int,
        todo_service: TodoService = Depends(Provide[Container.todo_service])
):
    return todo_service.get_by_id(todo_id)
