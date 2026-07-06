from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.webhook import router as webhook_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(webhook_router)

@app.get("/")
def home():
    return {
        "status": "online"
    }