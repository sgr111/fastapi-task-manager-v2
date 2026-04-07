from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

# Import models so Alembic can detect them
from app.models import task, user  # noqa: F401


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(api_router)

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok", "version": settings.APP_VERSION}

    return app


app = create_app()
