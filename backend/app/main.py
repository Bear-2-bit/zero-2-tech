from fastapi import FastAPI

from app.database import Base, engine
from app.models import task
from app.routers.tasks import router as tasks_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="zero-2-tech API"
)


app.include_router(tasks_router)


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok"
    }