import csv
import json

def process_csv_to_json(csv_file, quotes_json_file, authors_json_file):
    quotes = []
    authors = []
    
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Process quotes
            tags = [tag.strip() for tag in row['keywords'].split(',')]
            quote = {
                'tags': tags,
                'author': row['author'],
                'quote': row['quote']
            }
            quotes.append(quote)
            
            # Process authors
            author = {
                'fullname': row['author'],
                'born_date': row['born_date'],
                'born_location': row['born_location'],
                'description': row['description'],
            }
            authors.append(author)
    
    # Remove duplicates from authors
    authors = [dict(t) for t in {tuple(d.items()) for d in authors}]
    
    # Write to JSON files
    with open(quotes_json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(quotes, jsonfile, indent=4, ensure_ascii=False)
    
    with open(authors_json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(authors, jsonfile, indent=4, ensure_ascii=False)

# Виклик функції для обробки файлів
process_csv_to_json('result.csv', 'quotes.json', 'authors.json')
