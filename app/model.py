import dataclasses


@dataclasses.dataclass
class Todo:
    title: str
    is_completed: bool
    todo_id: int | None = None
