import json
from datetime import datetime
from mongoengine import connect
from models import Author, Quote
from bson import ObjectId

import configparser

def main():
    # Підключення до хмарної бази даних MongoDB
    config = configparser.ConfigParser()
    config.read('config.ini')

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    db_name = config.get('DB', 'db_name')
    domain = config.get('DB', 'domain')

    # connect to cluster on AtlasDB with connection string
    connect(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority", ssl=True)

    # Завантаження даних з JSON-файлів до бази даних
    load_authors_from_json('authors.json')
    load_quotes_from_json('quotes.json')


def load_authors_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            fullname = author_data['fullname']
            author = Author.objects(fullname=fullname).first()
            if author:
                # Оновлення існуючого запису
                author.update(
                    born_date=author_data['born_date'],
                    born_location=author_data['born_location'],
                    description=author_data['description']
                )
            else:
                # Створення нового запису
                author = Author(
                    fullname=fullname,
                    born_date=author_data['born_date'],
                    born_location=author_data['born_location'],
                    description=author_data['description']
                )
                author.save()

from bson import ObjectId

def load_quotes_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                quote_text = quote_data['quote']
                existing_quote = Quote.objects(author=author.id, quote=quote_text).first()
                if existing_quote:
                    print(f"Quote already exists: {quote_text}")
                else:
                    quote = Quote(
                        author=str(author.id),
                        quote=quote_text,
                        tags=quote_data.get('tags', [])
                    )
                    quote.save()
            else:
                print(f"Author '{author_name}' not found for quote: {quote_data['quote']}")


if __name__ == "__main__":
    main()
