print(">>> main.py is loaded <<<")

from fastapi import FastAPI
from src.app.presentation.api_router import api_router
from src.app.infrastructure.db.base import Base
from src.app.infrastructure.db.engine import engine

app = FastAPI(title="Shift Tasks API",
              version="0.0.5",
              description="API for creating updating and listing shift-based production tasks")

@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(engine)

app.include_router(api_router)