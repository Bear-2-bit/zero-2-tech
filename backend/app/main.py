from fastapi import FastAPI

from app.database import Base, engine
from app.models import task
from app.routers.tasks import router as tasks_router
from app.routers.auth import router as auth_router
from app.routers.ai import router as ai_router

app = FastAPI(
    title="zero-2-tech API"
)


app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(ai_router)

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok"
    }