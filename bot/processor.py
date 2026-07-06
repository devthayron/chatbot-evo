def process_message(raw_message):
    key = raw_message.get("key", {})
    remote_jid = key.get("remoteJid")
    from_me = key.get("fromMe")
    message_type = raw_message.get("messageType")
    timestamp = raw_message.get("messageTimestamp")
    push_name = raw_message.get("pushName")

    # Apenas mensagens de texto por enquanto
    if message_type != "conversation":
        return None

    message = raw_message.get("message", {}).get("conversation")

    # Número do contato da conversa
    number = (
        key.get("remoteJidAlt")
        or key.get("remoteJid", "")
    ).split("@")[0]

    return {
        "remoteJid": remote_jid,
        "number": number,
        "push_name": push_name,
        "from_me": from_me,
        "message": message,
        "message_type": message_type,
        "timestamp": timestamp,
    }