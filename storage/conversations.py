import json
from config import CONVERSATIONS_DIR

def save_conversation(message):
    number = message["number"]

    file_path = CONVERSATIONS_DIR / f"{number}.json"

    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            conversation = json.load(file)
    else:
        conversation = {
            "number": number,
            "push_name": message["push_name"],
            "messages": [],
        }

    if message["push_name"]:
        conversation["push_name"] = message["push_name"]

    conversation["messages"].append({
        "from_me": message["from_me"],
        "message": message["message"],
        "message_type": message["message_type"],
        "timestamp": message["timestamp"],
    })

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(conversation, file, ensure_ascii=False, indent=4)


def load_conversation(number):
    file_path = CONVERSATIONS_DIR / f"{number}.json"

    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)