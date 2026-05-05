from fastapi import FastAPI

app = FastAPI(title="Role-Based Notification System")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "message": "Hello from the notification server!"}
