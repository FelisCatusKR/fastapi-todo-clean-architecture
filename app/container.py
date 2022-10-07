from dependency_injector import containers, providers

from .database import InMemoryDatabase, SqlalchemyDatabase
from .repository import InMemoryTodoRepository, SqlalchemyTodoRepository
from .service import TodoService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".controller"])
    config = providers.Configuration(yaml_files=["config.yaml"])

    if config.environment() == "local" or config.environment() is None:
        db = providers.Singleton(InMemoryDatabase)
        todo_repository = providers.Factory(
            InMemoryTodoRepository,
            db=db,
        )

    else:
        from .orm import mapper_registry
        db = providers.Singleton(
            SqlalchemyDatabase,
            db_url=config.db.url(),
        )
        todo_repository = providers.Factory(
            SqlalchemyTodoRepository,
            session=db.provided.session,
        )

    todo_service = providers.Factory(
        TodoService,
        todo_repository=todo_repository,
    )
