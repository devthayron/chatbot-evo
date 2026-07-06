# chatbot-evo

Script em Python para extrair o histórico de mensagens de uma instância do WhatsApp conectada via [Evolution API](https://doc.evolution-api.com/) e armazenar cada conversa em um arquivo JSON separado.

## O que ele faz

- Busca as mensagens registradas em uma instância da Evolution API (`/chat/findMessages/{instance}`).
- Filtra apenas mensagens de texto (`conversation`), ignorando outros tipos (imagem, áudio, etc.).
- Processa cada mensagem individualmente.
- Salva cada conversa em um arquivo JSON separado dentro de `data/conversations/`, utilizando o número do contato como nome do arquivo.

---

## Envio de mensagem (teste)

Para enviar uma mensagem manualmente via Evolution API, edite o arquivo `tests/send_test.py` e substitua o número pelo real::

```python
from services.evolution import send_message

if __name__ == "__main__":
    numero = "5586999999999"  # substitua pelo número real
    texto = "enviando msg pelo python"

    send_message(numero, texto)
    print("Mensagem enviada!")
```

Execute o teste com:

```bash
python -m tests.send_test
```

---

## Arquitetura

```text

Evolution API (WhatsApp)
   ↓
get_messages()
   ↓
process_message()
   ↓
save_conversation()
   ↓
JSON por contato
```

---

## Estrutura do projeto

```text
chatbot-evo/
├── bot/
│   └── processor.py          # processamento das mensagens
├── data/
│   └── conversations/       # histórico separado por contato
├── services/
│   └── evolution.py         # integração com a Evolution API
├── storage/
│   └── conversations.py     # leitura e escrita das conversas
├── tests/
│   └── send_test.py
├── config.py
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Pré-requisitos

- Python 3.10+
- Uma instância ativa na Evolution API
- API Key da instância

---

## Instalação

```bash
git clone https://github.com/devthayron/chatbot-evo.git
cd chatbot-evo

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## Configuração

Copie o `.env.example` para `.env`:

```bash
cp .env.example .env
```

Preencha:

```env
BASE_URL=http://seu-servidor-evolution:8080
API_KEY_EVO=sua_api_key
INSTANCE=nome_da_instancia
```

| Variável       | Descrição                  |
| --------------- | ---------------------------- |
| `BASE_URL`    | URL base da Evolution API    |
| `API_KEY_EVO` | API Key da instância        |
| `INSTANCE`    | Nome da instância utilizada |

---

## Uso

Execute:

```bash
python main.py
```

Saída esperada:

```text
Mensagens processadas: 21
Mensagens ignoradas: 1
```

Após a execução, será criada a pasta:

```text
data/
└── conversations/
    ├── 5511999999999.json
    ├── 5586999999999.json
    └── 5599888888888.json
```

---

## Exemplo de arquivo de conversa

```json
{
    "number": "5599999999999",
    "push_name": "João",
    "messages": [
        {
            "from_me": false,
            "message": "Olá",
            "message_type": "conversation",
            "timestamp": 1783083116
        },
        {
            "from_me": true,
            "message": "Tudo bem?",
            "message_type": "conversation",
            "timestamp": 1783083150
        }
    ]
}
```

---

## Campos

- `number` → número do contato.
- `push_name` → nome do contato (quando disponível).
- `from_me`
  - `true` → mensagem enviada pela instância.
  - `false` → mensagem enviada pelo contato.
- `message` → conteúdo da mensagem.
- `message_type` → tipo da mensagem (atualmente apenas `conversation`).
- `timestamp` → horário da mensagem em formato Unix Timestamp.

---

## Autor

**Thayron Higlânder**

- LinkedIn: https://www.linkedin.com/in/thayron-higlander
