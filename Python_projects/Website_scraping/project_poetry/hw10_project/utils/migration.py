import os
import sys
import django

from pymongo import MongoClient

# Додаємо шлях до вашого проекту у список шляхів, які Python шукає модулі.
sys.path.append('C:\\Users\\Admin\\Downloads\\courses\\GoIT\\Python_for_Data_Science\\Python_WEB\\Projects\\HW_10\\project_poetry\\hw10_project')

# Завантажуємо Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw10_project.settings')

# Ініціалізуємо Django
django.setup()

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw10_project.settings")
# django.setup()

from quotes.models import Quote, Tag, Author # noqa

client = MongoClient("mongodb://localhost")

db = client.hw_10

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname = author['fullname'],
        born_date = author['born_date'],
        born_location = author['born_location'],
        description = author['description']
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exits_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))

    if not exits_quote:
        author = db.authors.find_one({'_id': quote['author']})
        a = Author.objects.get(fullname=author['fullname'])
        q = Quote.objects.create(
            quote = quote['quote'],
            author = a
        )
        for tag in tags:
            q.tags.add(tag)



    