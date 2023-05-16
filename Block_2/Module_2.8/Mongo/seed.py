from models import Author, Tag, Quote
import json

authors_obj = {}

with open('authors.json') as file:
    authors = json.loads(file.read())
    for author in authors:
        new_author = Author(
            fullname=author["fullname"],
            born_date=author["born_date"],
            born_location=author["born_location"],
            description=author["description"]
        )
        new_author.save()
        authors_obj[author["fullname"]] = new_author


with open('quotes.json') as file:
    quotes = json.loads(file.read())
    for quote in quotes:
        tags = [Tag(name=tag) for tag in quote["tags"]]
        new_quote = Quote(
            tags=tags,
            author=authors_obj[quote["author"]],
            quote=quote["quote"]
        )
        new_quote.save()
