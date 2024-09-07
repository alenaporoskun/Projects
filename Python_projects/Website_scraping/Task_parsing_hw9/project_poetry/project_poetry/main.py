import sys
from models import Quote, Author

from mongoengine import connect
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
    connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

    while True:
        command = input("Введіть команду: ").strip()
        
        if command.startswith("name:"):
            author_name = command.split(":")[1].strip()
            search_quotes_by_author(author_name)
        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            quotes = search_quotes_by_tag(tag)
            print_quotes(quotes)
        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip()
            quotes = search_quotes_by_tags(tags)
            print_quotes(quotes)
        elif command == "exit":
            sys.exit()
        else:
            print("Невідома команда. Спробуйте ще раз.")

def search_quotes_by_author(author_name):
    authors = Author.objects(fullname__icontains=author_name)
    if authors:
        for author in authors:
            search_quotes_by_author_name(author)
    else:
        print(f"Автора '{author_name}' не знайдено.")

def search_quotes_by_author_name(author):
    quotes = Quote.objects(author=str(author.id))
    if quotes:
        print(f"Цитати автора {author.fullname}:")
        for quote in quotes:
            print(f"- {quote.quote}")
    else:
        print(f"Цитати автора {author.fullname} не знайдено.")

def search_quotes_by_tag(tag):
    quotes = Quote.objects(tags__icontains=tag)
    return quotes

def search_quotes_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    return quotes

def print_quotes(quotes):
    for quote in quotes:
        print(quote.quote)

if __name__ == "__main__":
    main()
