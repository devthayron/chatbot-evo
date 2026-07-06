from fastapi import APIRouter, Request

from bot.processor import process_message
from services.openai import openai_service
from services.evolution import send_message
from storage.conversations import save_message, get_openai_history

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    raw_message = payload.get("data") or payload

    if isinstance(raw_message, list):
        raw_message = raw_message[0]

    message = process_message(raw_message)

    if not message or message["from_me"] or not message["message"]:
        return {"status": "ignored"}

    number = message["number"]
    push_name = message["push_name"]
    user_text = message["message"]

    # 1. SALVA MENSAGEM DO USUÁRIO (cria o JSON se não existir), com o timestamp do WhatsApp
    conversation = save_message(
        number=number,
        push_name=push_name,
        from_me=False,
        content=user_text,
        timestamp=message["timestamp"],
    )

    # 2. MONTA HISTÓRICO NO FORMATO role/content (a instrução de sistema já vai via `instructions`)
    messages = get_openai_history(conversation)

    # 3. IA RESPONDE COM MEMÓRIA COMPLETA
    response = openai_service.generate_response(messages)

    # 4. SALVA RESPOSTA DA IA (timestamp próprio, do momento da resposta)
    save_message(
        number=number,
        push_name=push_name,
        from_me=True,
        content=response,
    )

    # 5. ENVIA RESPOSTA
    send_message(number=number, text=response)

    return {"status": "processed"}