from dependency_injector import containers, providers

from .service import TodoService
from .uow import InMemoryTodoUnitOfWork, SqlalchemyTodoUnitOfWork


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".controller"])
    config = providers.Configuration(yaml_files=["config.yaml"])

    if config.environment() == "local" or config.environment() is None:
        todo_uow = providers.Singleton(InMemoryTodoUnitOfWork)

    else:
        from .orm import mapper_registry
        todo_uow = providers.Singleton(SqlalchemyTodoUnitOfWork)

    todo_service = providers.Factory(
        TodoService,
        todo_uow=todo_uow,
    )
