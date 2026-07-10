# Chatbot WhatsApp com IA

Sistema de chatbot integrado ao WhatsApp através da Evolution API, capaz de receber mensagens, identificar usuários, manter o histórico das conversas e gerar respostas automáticas utilizando inteligência artificial com base no contexto da conversa.

---

# Funcionalidades

* Integração entre WhatsApp, Evolution API, inteligência artificial e banco de dados
* Recebimento e processamento de mensagens via webhook
* Identificação de usuários e armazenamento do histórico de conversas
* Importação automática do histórico existente no primeiro contato
* Recuperação de contexto para respostas mais precisas
* Geração de respostas automáticas utilizando OpenAI
* Controle de mensagens duplicadas
* Envio automático de respostas pelo WhatsApp

---

# Histórico de conversas

Quando um usuário envia uma mensagem:

1. A mensagem chega pelo WhatsApp através da Evolution API e o sistema identifica o contato pelo número.
2. O sistema verifica se já existe histórico desse usuário armazenado no banco de dados.
3. Caso o histórico já exista, as mensagens salvas são utilizadas como contexto para a conversa.
4. Caso não exista histórico, o sistema busca as mensagens antigas desse contato na Evolution API.
5. As mensagens encontradas são organizadas por data e armazenadas no banco.
6. Após a primeira importação, o histórico salvo passa a ser reutilizado nas próximas interações.

> A importação acontece apenas no primeiro contato de cada usuário, evitando consultas desnecessárias à Evolution API.

---

# Fluxo da aplicação

```text
WhatsApp
    |
    ▼
Evolution API
    |
    ▼
Webhook
    |
    ▼
Processamento da mensagem
    |
    ▼
Identificar usuário
    |
    ▼
Verificar histórico
    |
    +----------------+
    |                |
    ▼                ▼
Existe histórico   Primeiro contato
    |                |
    ▼                ▼
Usa histórico    Importa conversas
do banco         da Evolution API
    |                |
    +--------+-------+
             |
             ▼
        Buscar contexto
             |
             ▼
          OpenAI
             |
             ▼
       Gerar resposta
             |
             ▼
      Salvar resposta
             |
             ▼
Enviar resposta no WhatsApp
```

---

# Estrutura do projeto

```text

chatbot/
├── app/                            # aplicação e rotas da API
│   ├── main.py
│   └── routes/
│       ├── webhook.py
│       └── chat.py
│
├── bot/                            # processamento das mensagens
│   └── message_processor.py
│
├── services/                       # integrações e regras do sistema
│   ├── chatbot.py
│   ├── evolution.py
│   └── openai.py
│
├── database/                       # modelos e operações do banco de dados
│   ├── connection.py
│   ├── models.py
│   ├── users.py
│   └── conversations.py
│
├── data/                            # arquivos de dados da aplicação
│   └── conversations.db
│
├── config.py
├── requirements.txt
└── README.md
```

---

# Tecnologias

* Python 3.12
* FastAPI
* OpenAI API
* Evolution API
* SQLAlchemy
* SQLite

---

# Banco de dados

SQLite é utilizado inicialmente para armazenar usuários e histórico das conversas.

```text
data/
└── conversations.db
```

---

# Tabelas

## Usuários (`users`)

| Campo  | Descrição               |
| ------ | ------------------------- |
| id     | Identificador do usuário |
| name   | Nome do contato           |
| number | Número do WhatsApp       |

---

## Mensagens (`messages`)

| Campo        | Descrição                      |
| ------------ | -------------------------------- |
| id           | Identificador interno            |
| message_id   | Identificador único da mensagem |
| user_id      | Usuário relacionado             |
| role         | Usuário ou assistente           |
| content      | Texto da mensagem                |
| message_type | Tipo da mensagem                 |
| sent_at      | Data e hora                      |

---

# Instalação

```bash
git clone https://github.com/devthayron/chatbot-evo.git

cd chatbot-evo

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

# Configuração

Criar `.env`:

```env
OPENAI_API_KEY=

BASE_URL=
INSTANCE=
API_KEY_EVO=
```

Variáveis:

| Variável      | Descrição                |
| -------------- | -------------------------- |
| OPENAI_API_KEY | Chave da OpenAI            |
| BASE_URL       | Endereço da Evolution API |
| INSTANCE       | Instância do WhatsApp     |
| API_KEY_EVO    | Chave da Evolution API     |

---

# Executando

Para executar a aplicação localmente:

```bash
uvicorn app.main:app --reload
```

Swagger:

```
http://localhost:8000/docs
```

---

# Desenvolvimento

Durante o desenvolvimento, a aplicação FastAPI roda localmente e utiliza ngrok para expor o webhook publicamente, permitindo a comunicação com a Evolution API.

Mais detalhes sobre execução local e configuração do ambiente estão disponíveis em:

[Documentação de desenvolvimento](docs/dev.md)

# Próximos passos:

# Próximos passos

- Testes automatizados
- Sistema de logs
- Dockerização da aplicação
- Migração para PostgreSQL
- Dashboard administrativo
- RAG com documentos

---

# Autor

**Thayron Higlânder Santos**

LinkedIn:
[https://www.linkedin.com/in/thayron-higlander](https://www.linkedin.com/in/thayron-higlander)
