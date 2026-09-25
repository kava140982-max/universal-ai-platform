from fastapi import FastAPI
from universal_ai.api.routes import router

def create_app() -> FastAPI:
    app = FastAPI(title="Universal AI Platform", version="0.1.0")
    app.include_router(router)
    return app