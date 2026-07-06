import json
import os
import tempfile
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from config import CONVERSATIONS_DIR
from services.evolution import get_messages_by_number
from bot.processor import process_message

TIMEZONE = ZoneInfo("America/Sao_Paulo")


def _default_conversation(number, push_name):
    return {
        "number": number,
        "push_name": push_name,
        "messages": [],
    }


def _file_path(number):
    return CONVERSATIONS_DIR / f"{number}.json"


def load_conversation(number):
    file_path = _file_path(number)

    if not file_path.exists():
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return None


def _write_conversation(number, conversation):
    file_path = _file_path(number)

    tmp_fd, tmp_path = tempfile.mkstemp(dir=CONVERSATIONS_DIR, suffix=".tmp")
    with os.fdopen(tmp_fd, "w", encoding="utf-8") as file:
        json.dump(conversation, file, ensure_ascii=False, indent=2)
    os.replace(tmp_path, file_path)


def _import_history_from_evolution(number, push_name):
    """
    Busca o histórico antigo direto na Evolution API pra esse número
    e monta a conversa já no formato role/content/timestamp.
    Usado só na primeira vez que o número aparece (sem JSON local ainda).
    """
    conversation = _default_conversation(number, push_name)

    try:
        registros = get_messages_by_number(number)
    except Exception as e:
        print(f"Falha ao importar histórico da Evolution API pra {number}: {e}")
        return conversation

    for registro in registros:
        msg = process_message(registro)
        if not msg or not msg["message"]:
            continue

        conversation["messages"].append({
            "role": "assistant" if msg["from_me"] else "user",
            "content": msg["message"],
            "timestamp": msg["timestamp"],
        })

    conversation["messages"] = conversation["messages"][-30:]

    return conversation


def save_message(number, push_name, from_me, content, timestamp=None):
    """
    Carrega a conversa (importando histórico antigo se for a primeira vez),
    adiciona a mensagem no formato role/content/timestamp e salva no JSON.
    Retorna a conversa atualizada.
    """
    if not content:
        return load_conversation(number) or _default_conversation(number, push_name)

    conversation = load_conversation(number)

    if conversation is None:
        conversation = _import_history_from_evolution(number, push_name)

    if push_name:
        conversation["push_name"] = push_name

    conversation["messages"].append({
        "role": "assistant" if from_me else "user",
        "content": content,
        "timestamp": timestamp or int(time.time()),
    })

    conversation["messages"] = conversation["messages"][-30:]

    _write_conversation(number, conversation)

    return conversation


def _format_timestamp(ts):
    dt = datetime.fromtimestamp(ts, tz=TIMEZONE)
    return dt.strftime("%d/%m/%Y %H:%M")


def get_openai_history(conversation, limit=20):
    if not conversation:
        return []

    history = []
    for msg in conversation["messages"][-limit:]:
        time_prefix = f"[{_format_timestamp(msg['timestamp'])}] "
        history.append({
            "role": msg["role"],
            "content": time_prefix + msg["content"],
        })

    return history