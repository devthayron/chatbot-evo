from services.evolution import get_messages
from bot.processor import process_message
from storage.conversations import save_conversation


def main():
    raw_messages = get_messages()

    processed_count = 0
    ignored_count = 0

    for raw_message in raw_messages:
        processed_message = process_message(raw_message)

        if processed_message is None:
            ignored_count += 1

            message_type = raw_message.get("messageType")
            print(f"Mensagem ignorada (tipo diferente de texto): {message_type}")

            continue

        save_conversation(processed_message)
        processed_count += 1

    print(f"\nResumo:")
    print(f"- Processadas: {processed_count}")
    print(f"- Ignoradas: {ignored_count}")


if __name__ == "__main__":
    main()