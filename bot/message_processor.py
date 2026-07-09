def extract_webhook_message(payload):

    # Processa apenas novas mensagens recebidas
    if payload.get("event") != "messages.upsert":
        return None

    raw_message = payload.get("data")

    if not raw_message:
        return None

    # Pega msg apenas do usuario aceita apenas fromMe=False
    if raw_message.get("key", {}).get("fromMe"):
        return None

    return raw_message


def handle_text(raw_message):
    return raw_message.get("message", {}).get("conversation")

def handle_image(raw_message):
    return "[Imagem enviada pelo usuário]"

def handle_audio(raw_message):
    return "[Áudio enviado pelo usuário]"

MESSAGE_TYPE_HANDLERS = {
        "conversation": handle_text,
        "imageMessage": handle_image,
        "audioMessage": handle_audio,
    }

def handle_message_type(raw_message):
    message_type = raw_message.get("messageType")

    handle = MESSAGE_TYPE_HANDLERS.get(message_type)

    if handle:
        return message_type, handle(raw_message)

    return message_type, f"[Mensagem do tipo: {message_type}]"


def normalize_message(raw_message):
    
    key = raw_message.get("key", {})
    remote_jid = key.get("remoteJid")
    remote_jid_alt = key.get("remoteJidAlt")
    timestamp = raw_message.get("messageTimestamp")
    push_name = raw_message.get("pushName")

    # Apenas mensagens de texto por enquanto
    message_type, message = handle_message_type(raw_message)
    
    # Número do contato da conversa
    number = remote_jid_alt or remote_jid
    
    if number is None:
        return None

    number = number.split("@")[0]

    return {
        "remoteJid": remote_jid,
        "number": number,
        "push_name": push_name,
        "message": message,
        "message_type": message_type,
        "timestamp": timestamp,
    }

