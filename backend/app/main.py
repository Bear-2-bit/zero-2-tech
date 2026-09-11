from fastapi import FastAPI


app = FastAPI(
    title="zero-2-tech API"
)


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok"
    }