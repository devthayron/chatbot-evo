from fastapi import APIRouter
from app.schemas.message import ChatRequest
from services.openai import openai_service

router = APIRouter()


@router.post("/chat")
def chat(data: ChatRequest):
    response = openai_service.generate_response(data.message)

    return {
        "response": response
    }