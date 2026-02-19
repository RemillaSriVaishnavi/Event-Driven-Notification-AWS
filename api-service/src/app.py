from fastapi import FastAPI
from src.routes.events import router as event_router

app = FastAPI()

app.include_router(event_router)
