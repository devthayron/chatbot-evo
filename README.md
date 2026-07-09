# Chatbot WhatsApp com IA

Chatbot para WhatsApp desenvolvido em Python utilizando **FastAPI**, **Evolution API**, **OpenAI API**, **SQLAlchemy** e **SQLite**.

A aplicação recebe mensagens através da Evolution API, armazena o histórico das conversas em banco de dados, utiliza esse contexto para gerar respostas com a OpenAI e envia automaticamente a resposta ao usuário pelo WhatsApp.
---

## Funcionalidades

* Integração com Evolution API
* Webhook para recebimento de mensagens do WhatsApp
* Processamento e normalização de mensagens recebidas
* Integração com OpenAI API
* Armazenamento de usuários e histórico de mensagens em SQLite
* Recuperação automática de contexto para conversas
* Geração de respostas utilizando histórico anterior
* Envio automático de respostas pelo WhatsApp
* Estrutura modular para facilitar manutenção e evolução do projeto

---

## Fluxo da aplicação

```text
WhatsApp
    |
    ▼
Evolution API
    |
    ▼
Webhook FastAPI
    |
    ▼
Message Processor
    |
    ▼
Mensagem normalizada
    |
    +----------------+
    |                |
    ▼                ▼
SQLite          Histórico
    |                |
    +-------+--------+
            |
            ▼
        OpenAI API
            |
            ▼
     Resposta gerada
            |
            ▼
     Salvar resposta
            |
            ▼
     Evolution API
            |
            ▼
        WhatsApp
```

---

## Estrutura do projeto

```text
chatbot/
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── webhook.py       
│   │   └── chat.py          
│   └── schemas/
│       └── message.py      
│
├── bot/
│   └── message_processor.py # processamento e normalização das mensagens
│
├── services/
│   ├── chatbot.py           # fluxo principal da conversa com IA
│   ├── evolution.py         # integração com Evolution API
│   └── openai.py            # integração com OpenAI API
│
├── database/
│   ├── connection.py        # conexão SQLAlchemy
│   ├── models.py            # modelos ORM
│   └── conversations.py     # operações de persistência
│
├── data/
│   └── conversations.db     # banco SQLite
│
├── config.py
├── requirements.txt
└── README.md
```

---

## Tecnologias

* Python 3.12
* FastAPI
* OpenAI API
* Evolution API
* SQLAlchemy
* SQLite
* Uvicorn
* python-dotenv

---

## Funcionamento

Quando uma mensagem é recebida:

1. A Evolution API envia o evento para o webhook da aplicação.
2. O webhook valida o evento recebido para aceitar apenas eventos `messages.upsert`, responsáveis pela criação/recebimento de novas mensagens.
3. O `message_processor` filtra e transforma a mensagem recebida em um formato normalizado.
4. A mensagem do usuário é salva no banco.
5. O histórico da conversa é recuperado.
6. O histórico é enviado para a OpenAI como contexto.
7. A resposta gerada pela IA é armazenada.
8. A resposta é enviada ao usuário através da Evolution API.

---

## Instalação

Clone o projeto:

```bash
git clone https://github.com/devthayron/chatbot-evo.git
cd chatbot-evo
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente:

Linux:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=

BASE_URL=
INSTANCE=
API_KEY_EVO=
```

Variáveis:

| Variável         | Descrição                              |
| ---------------- | -------------------------------------- |
| `OPENAI_API_KEY` | Chave da OpenAI API                    |
| `BASE_URL`       | URL da Evolution API                   |
| `INSTANCE`       | Nome da instância do WhatsApp          |
| `API_KEY_EVO`    | Chave de autenticação da Evolution API |

---

## Executando

Inicie a aplicação:

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

Documentação automática:

```text
http://localhost:8000/docs
```

---

# Banco de dados

O sistema utiliza SQLite para persistência inicial.

Banco:

```text
data/
└── conversations.db
```

## Modelo de dados

### Tabela `users`

| Campo  | Tipo    | Descrição           |
| ------ | ------- | ------------------- |
| id     | INTEGER | Identificador único |
| name   | TEXT    | Nome do contato     |
| number | TEXT    | Número do WhatsApp  |

---

### Tabela `conversations`

| Campo        | Tipo     | Descrição                                               |
| ------------ | -------- | ------------------------------------------------------- |
| id           | INTEGER  | Identificador único da mensagem                         |
| user_id      | INTEGER  | Referência ao usuário                                   |
| role         | TEXT     | Origem da mensagem (`user` ou `assistant`)              |
| content      | TEXT     | Conteúdo da mensagem                                    |
| message_type | TEXT     | Tipo da mensagem (`conversation`, `imageMessage`, etc.) |
| timestamp    | DATETIME | Data e hora da mensagem                                 |

---

## Relacionamento

| Origem     | Destino                | Cardinalidade |
| ---------- | ---------------------- | ------------- |
| `users.id` | `conversation.user_id` | 1:N           |

Um usuário pode possuir várias mensagens no histórico.

Esse histórico é utilizado como contexto antes da geração de uma nova resposta pela IA.
> Somente as ultimas 30 mensagens como padrão 

---

## Próximos passos

* Suporte a múltiplas instâncias do WhatsApp
* Migração para PostgreSQL
* Memória de longo prazo
* Sistema RAG com documentos
* Painel administrativo
* Testes automatizados
* Logging estruturado para auditoria

---

## Autor

**Thayron Higlânder Santos**

LinkedIn:
https://www.linkedin.com/in/thayron-higlander
