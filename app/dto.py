from pydantic import BaseModel


class TodoCreateDto(BaseModel):
    title: str
    is_completed: bool = False
