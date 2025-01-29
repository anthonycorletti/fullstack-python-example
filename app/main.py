import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Union

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from app import __version__
from app.exceptions import exception_handlers
from app.kit.router import respond_to
from app.kit.sqlite import create_async_engine, create_async_sessionmaker
from app.pages.index import IndexPage
from app.pages.not_found import NotFoundPage
from app.router import app_router
from app.settings import ResponseFormat, settings

os.environ["TZ"] = "UTC"

log = structlog.get_logger()


def configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_session_middleware(app: FastAPI) -> None:
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.API_SECRET_KEY,
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    log.debug("starting up")
    asyncengine = create_async_engine("app")
    asyncsessionmaker = create_async_sessionmaker(asyncengine)
    yield {"asyncengine": asyncengine, "asyncsessionmaker": asyncsessionmaker}
    await asyncengine.dispose()
    log.debug("shutting down")


def create_fastapi_app() -> FastAPI:
    app = FastAPI(
        title="fullstack-python-example",
        version=__version__,
        lifespan=lifespan,
        exception_handlers=exception_handlers,
    )
    app.include_router(app_router)

    @app.get("/", response_model=Dict)
    async def _index(request: Request) -> Union[HTMLResponse, Dict]:
        return await respond_to(
            request,
            {
                ResponseFormat.json: {"data": {"message": "hey!"}},
                ResponseFormat.html: {"data": [], "page": IndexPage},
            },
        )

    @app.get("/404", response_model=Dict)
    async def _not_found(request: Request) -> Union[HTMLResponse, Dict]:
        return await respond_to(
            request,
            {
                ResponseFormat.json: {
                    "data": {"message": "this is not the page you are looking for!"}
                },
                ResponseFormat.html: {"data": [], "page": NotFoundPage},
            },
        )

    configure_cors(app)
    return app


app = create_fastapi_app()
