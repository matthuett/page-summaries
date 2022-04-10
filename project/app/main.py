import logging

from fastapi import FastAPI
from .api import ping, summaries
from .db import create_db_tables

log = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
    return application


app = create_app()


@app.on_event("startup")
def startup():
    log.info("Starting up application...")
    create_db_tables()


@app.on_event("shutdown")
def shutdown():
    log.info("Shutting down application...")
