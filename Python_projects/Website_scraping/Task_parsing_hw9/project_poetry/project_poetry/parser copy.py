import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {"FEED_FORMAT": "csv", "FEED_URI": "result.csv"}

    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            # Отримуємо дані про цитату
            keywords = quote.xpath("div[@class='tags']/a/text()").extract()
            quote_text = quote.xpath("span[@class='text']/text()").get()

            # Отримуємо ім'я автора та URL його сторінки
            author_name = quote.xpath("span/small/text()").get()
            author_url = quote.xpath("span/small/following-sibling::a/@href").get()
            author_url = response.urljoin(author_url)

            # Переходимо на сторінку автора, щоб отримати додаткову інформацію
            yield scrapy.Request(author_url, callback=self.parse_author, meta={'keywords': keywords, 'quote': quote_text, 'author': author_name})

        # Переходимо на наступну сторінку, якщо вона є
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_author(self, response):
        # Отримуємо дані про автора
        born_date = response.xpath("//strong[text()='Born:']/following-sibling::span[@class='author-born-date']/text()").get()
        born_location = response.xpath("//strong[text()='Born:']/following-sibling::span[@class='author-born-location']/text()").get()
        born_location = born_location.replace('in ', '')
        description = response.xpath("//div[@class='author-description']/text()").get()

        # Отримуємо дані про цитату
        quote = response.meta['quote']
        keywords = response.meta['keywords']
        author = response.meta['author']

        # Повертаємо дані
        yield {
            'keywords': keywords,
            'author': author,
            'born_date': born_date,
            'born_location': born_location,
            'description': description,
            'quote': quote
        }



# Запускаємо парсер
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
