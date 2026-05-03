"""Simple GraphQL Book Service demo.

Run:
    pip install fastapi uvicorn graphene
    uvicorn graphql_server:app --reload
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

import graphene
from fastapi import FastAPI
from pydantic import BaseModel


@dataclass
class BookModel:
    id: str
    title: str
    author: str
    published_year: int


BOOKS: dict[str, BookModel] = {}


class Book(graphene.ObjectType):
    id = graphene.String(required=True)
    title = graphene.String(required=True)
    author = graphene.String(required=True)
    published_year = graphene.Int(required=True)


class Query(graphene.ObjectType):
    book = graphene.Field(Book, id=graphene.String(required=True))
    books = graphene.List(Book)

    def resolve_book(self, info, id: str):
        return BOOKS.get(id)

    def resolve_books(self, info):
        return list(BOOKS.values())


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        published_year = graphene.Int(required=True)

    Output = Book

    def mutate(self, info, title: str, author: str, published_year: int):
        book = BookModel(str(uuid.uuid4()), title, author, published_year)
        BOOKS[book.id] = book
        return book


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        title = graphene.String()
        author = graphene.String()
        published_year = graphene.Int()

    Output = Book

    def mutate(self, info, id: str, title=None, author=None, published_year=None):
        book = BOOKS.get(id)
        if not book:
            raise ValueError("Book not found")
        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if published_year is not None:
            book.published_year = published_year
        return book


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean(required=True)

    def mutate(self, info, id: str):
        deleted = BOOKS.pop(id, None)
        return DeleteBook(ok=deleted is not None)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
app = FastAPI(title="Book GraphQL API Demo")


class GraphQLRequest(BaseModel):
    query: str
    variables: dict | None = None


@app.post("/graphql")
def graphql_endpoint(payload: GraphQLRequest):
    result = schema.execute(payload.query, variable_values=payload.variables)
    response = {}
    if result.errors:
        response["errors"] = [str(err) for err in result.errors]
    if result.data is not None:
        response["data"] = result.data
    return response


@app.get("/")
def root():
    return {"status": "ok", "books_count": len(BOOKS)}


@app.get("/health")
def health():
    return {"status": "ok"}
