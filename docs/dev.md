# Ambiente de desenvolvimento

Durante o desenvolvimento, a aplicação FastAPI roda localmente e o webhook é disponibilizado publicamente utilizando o ngrok.

A Evolution API pode ser executada em diferentes ambientes:

- **VPS:** mais próximo de um ambiente de produção.
- **Máquina local:** utilizado para testes e desenvolvimento.
- **Outros ambientes de hospedagem:** conforme a necessidade do projeto.

Neste projeto, a Evolution API está **hospedada em uma VPS**, enquanto o FastAPI é executado localmente durante o desenvolvimento.

---

# Fluxo de desenvolvimento

```text
WhatsApp
    |
    ▼
Evolution API (VPS)
    |
    ▼
ngrok (URL pública)
    |
    ▼
FastAPI (computador local)
    |
    ▼
SQLite local
````

---

# Executando a aplicação

## Terminal 1 — iniciar o FastAPI

```bash
uvicorn app.main:app --reload
```

## Terminal 2 — criar túnel público com ngrok

```bash
ngrok http 8000
```

O ngrok irá gerar uma URL pública:

```text
https://xxxx.ngrok-free.app
```

Essa URL deve ser configurada como webhook na Evolution API:

```text
https://xxxx.ngrok-free.app/webhook/
```

> Durante o desenvolvimento, a URL do ngrok pode mudar a cada execução dependendo da configuração utilizada.

---

# Banco de dados

Durante o desenvolvimento, o projeto utiliza SQLite por ser simples e não exigir configuração adicional.

O banco fica armazenado localmente:

```text
data/
└── conversations.db
```

---

# Ambiente de produção

Em produção, o recomendado é executar a aplicação em uma infraestrutura própria, removendo a necessidade do ngrok.

A Evolution API, o FastAPI e o banco de dados podem ser hospedados em uma VPS.

Fluxo:

```text
WhatsApp
    |
    ▼
Evolution API (VPS)
    |
    ▼
FastAPI (VPS)
    |
    ▼
PostgreSQL
```

O PostgreSQL é recomendado para produção devido a:

* Maior capacidade de armazenamento.
* Melhor desempenho com maior volume de mensagens.
* Maior segurança e controle dos dados.
* Facilidade para backups e manutenção.

---

# Observação

O ngrok é utilizado apenas durante o desenvolvimento, pois cria um acesso público temporário para uma aplicação que está rodando localmente.

Em ambientes de produção, o recomendado é utilizar uma hospedagem própria com domínio, HTTPS e um banco de dados adequado.

---

# Comparação dos ambientes

## Desenvolvimento

```text
Evolution API (VPS ou local)
        |
        ▼
ngrok
        |
        ▼
FastAPI local
        |
        ▼
SQLite
```

## Produção

```text
Evolution API (VPS)
        |
        ▼
FastAPI (VPS)
        |
        ▼
PostgreSQL
```
