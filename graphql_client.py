"""Client demo for the GraphQL Book service."""

from __future__ import annotations

import requests

GRAPHQL_URL = "http://127.0.0.1:8000/graphql"


def run_query(query: str, variables: dict | None = None):
    payload = {"query": query, "variables": variables or {}}
    response = requests.post(GRAPHQL_URL, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def main():
    create_mutation = """
    mutation CreateBook($title: String!, $author: String!, $publishedYear: Int!) {
      createBook(title: $title, author: $author, publishedYear: $publishedYear) {
        id
        title
        author
        publishedYear
      }
    }
    """
    created = run_query(
        create_mutation,
        {"title": "1984", "author": "George Orwell", "publishedYear": 1949},
    )
    print("CREATE:", created)

    book_id = created["data"]["createBook"]["id"]

    get_query = """
    query GetBook($id: String!) {
      book(id: $id) {
        id
        title
        author
        publishedYear
      }
    }
    """
    print("GET:", run_query(get_query, {"id": book_id}))

    update_mutation = """
    mutation UpdateBook($id: String!, $title: String!) {
      updateBook(id: $id, title: $title) {
        id
        title
        author
        publishedYear
      }
    }
    """
    print("UPDATE:", run_query(update_mutation, {"id": book_id, "title": "Nineteen Eighty-Four"}))

    list_query = """
    query {
      books {
        id
        title
        author
        publishedYear
      }
    }
    """
    print("LIST:", run_query(list_query))

    delete_mutation = """
    mutation DeleteBook($id: String!) {
      deleteBook(id: $id) {
        ok
      }
    }
    """
    print("DELETE:", run_query(delete_mutation, {"id": book_id}))


if __name__ == "__main__":
    main()
