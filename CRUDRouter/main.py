import time
from fastapi import FastAPI, Request
from core.logging_config import setup_logging
from core.database import create_db_and_tables
from routers.user import user

app = FastAPI()

setup_logging()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.include_router(user)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time())
    return response