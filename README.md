# GraphQL Book Service Demo (Python)

This demo includes:
- `graphql_server.py`: GraphQL API with CRUD operations for books.
- `graphql_client.py`: Simple client script that calls create/get/update/list/delete.
- `book_service.proto`: Proto definition for equivalent Book service contract.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run server

```bash
uvicorn graphql_server:app --reload
```

GraphQL endpoint: `http://127.0.0.1:8000/graphql`

## Run client

```bash
python graphql_client.py
```
