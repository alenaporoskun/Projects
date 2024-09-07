## Домашнє завдання #9


## Завдання 1

Виберіть бібліотеку BeautifulSoup або фреймворк Scrapy. Ви повинні виконати скрапінг сайту [quotes.toscrape.com](http://quotes.toscrape.com). Ваша мета отримати два файли: qoutes.json, куди помістіть всю інформацію про цитати, з усіх сторінок сайту та authors.json, де буде знаходитись інформація про авторів зазначених цитат. Структура файлів json повинна повністю збігатися з попереднього домашнього завдання. Виконайте раніше написані скрипти для завантаження json файлів у хмарну базу даних для отриманих файлів. Попередня домашня робота повинна коректно працювати з новою отриманою базою даних.


### Порядок виконання

Щоб створити віртуальне середовище і запустити його:  
```poetry new project_poetry```  
```cd project_poetry```   
```poetry shell```   
```poetry add Scrapy```   
```poetry add mongoengine```   
```scrapy startproject project_spyder```   
```cd project_spyder```   
```scrapy genspider authors quotes.toscrape.com```    
```cd ..```  
```cd project_poetry```  
```poetry run python parser.py```   
```poetry run python process_csv_to_json.py```    
```poetry run python load_json.py```   
```poetry run python main.py```    

Якщо віртуальне середовище вже створене:  

```cd project_poetry```  
```poetry shell```  
```cd project_poetry```  
```poetry run python parser.py```  
```poetry run python process_csv_to_json.py```  
```poetry run python load_json.py```  
```poetry run python main.py```  


### Опис необхідних скриптів

1. [parser.py](project_poetry/project_poetry/parser.py) - скрипт для парсингу днаих з сайту [quotes.toscrape.com](http://quotes.toscrape.com)
2. ```process_csv_to_json.py``` - скрипт для завантаження результату парсингу у формат json
3. ```load_json.py``` - скрипт для завантаження json файлів у хмарну базу даних Atlas MongoDB [cloud.mongodb.com](https://cloud.mongodb.com/v2/65d9a32ed4925f3961ccb339#/overview)
5. ```main.py``` -  скрипт для пошуку цитат за тегом, за ім'ям автора або набором тегів. Скрипт виконується в нескінченному циклі і за допомогою звичайного оператора input приймає команди у наступному форматі команда: значення.   
Приклад:
```name: Steve Martin``` — знайти та повернути список всіх цитат автора Steve Martin;  
```tag:life``` — знайти та повернути список цитат для тега life;   
```tags:life,live``` — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);  
```exit``` — завершити виконання скрипту

Виведення результатів пошуку лише у форматі utf-8.

## Результат 

Результат виконання файлу ```main.py```:    
```
(project-poetry-py3.10) PS C:\Users\Admin\Downloads\courses\GoIT\Python_for_Data_Science\Python_WEB\Projects\HW_9\Task_1\project_poetry\project_poetry>   poetry run python main.py  
Введіть команду: name:W.C. Fields  
Цитати автора W.C. Fields:  
- “I am free of all prejudice. I hate everyone equally. ”  
Введіть команду: name:J.K. Rowling  
Цитати автора J.K. Rowling:  
- “It is our choices, Harry, that show what we truly are, far more than our abilities.”   
Введіть команду: name:William Nicholson  
Цитати автора William Nicholson:  
- “We read to know we're not alone.”  
Введіть команду: exit  
```


