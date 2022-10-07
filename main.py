import uvicorn
from fastapi import FastAPI

from app import controller
from app.container import Container

container = Container()

app = FastAPI()
app.container = container
app.include_router(controller.router)

if __name__ == "__main__":
    uvicorn.run(app)
