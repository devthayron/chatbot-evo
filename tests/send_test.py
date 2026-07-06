from services.evolution import send_message

if __name__ == "__main__":
    numero = "5599988040698"   # substitue pelo número real
    texto = "enviando msg pelo python"
    send_message(numero, texto)
    print('Mensagem enviada!') 