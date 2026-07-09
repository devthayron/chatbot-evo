from services.openai import openai_service
from database.conversations import (
    save_message,
    get_openai_history,
)


def process_conversation(
    *,
    number: str,
    push_name: str | None,
    message: str,
    timestamp: int | None = None,
    message_type: str,
) -> str:
    """
    Processa uma conversa com a IA.

    - Salva a mensagem recebida.
    - Monta o histórico.
    - Gera a resposta da IA.
    - Salva a resposta.
    """

    user = save_message(
        number=number,
        push_name=push_name,
        from_me=False,
        content=message,
        timestamp=timestamp,
        message_type=message_type
    )

    history = get_openai_history(user)

    response = openai_service.generate_response(history)

    save_message(
        number=number,
        push_name=push_name,
        from_me=True,
        content=response,
    )

    return response