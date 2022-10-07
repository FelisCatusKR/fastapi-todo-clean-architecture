from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean
from sqlalchemy.orm import registry

from model import Todo

metadata = MetaData()

todo = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("title", Boolean, nullable=False),
)

mapper_registry = registry()
mapper_registry.map_imperatively(Todo, todo)
