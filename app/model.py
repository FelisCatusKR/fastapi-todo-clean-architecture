import dataclasses
from uuid import UUID, uuid4


@dataclasses.dataclass(frozen=True)
class Todo:
    title: str
    is_completed: bool
    todo_id: UUID = dataclasses.field(default_factory=uuid4)
