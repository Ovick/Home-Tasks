import json
import scrapy
from itemadapter import ItemAdapter
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess


class QuoteItem(Item):
    author = Field()
    quote = Field()
    tags = Field()


class AuthorItem(Item):
    fullname = Field()
    birth_date = Field()
    birth_location = Field()
    description = Field()


class LinkItem(Item):
    next_link = Field()


class SpiderPipeline(object):
    quotes = []
    authors = []
    links = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'author' in adapter.keys():
            self.quotes.append({
                "author": adapter["author"],
                "quote": adapter["quote"],
                "tags": adapter["tags"]
            })
        if 'fullname' in adapter.keys():
            self.authors.append({
                "fullname": adapter["fullname"],
                "birth_date": adapter["birth_date"],
                "birth_location": adapter["birth_location"],
                "description": adapter["description"]
            })
        if 'next_link' in adapter.keys():
            self.links.append({
                "next_link": adapter["next_link"]
            })
        return item

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False)
        with open('authors.json', 'w', encoding='utf-8') as fd:
            json.dump(self.authors, fd, ensure_ascii=False)
        with open('links.json', 'w', encoding='utf-8') as fd:
            json.dump(self.links, fd, ensure_ascii=False)


class Spider(scrapy.Spider):
    name = 'my_spider'
    custom_settings = {
        "ITEM_PIPELINES": {
            SpiderPipeline: 500
        }
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for text in response.xpath('/html//div[@class="quote"]'):
            quote = text.xpath('span[@class="text"]/text()').get().strip()
            author = text.xpath(
                'span/small[@class="author"]/text()').get().strip()
            tags = text.xpath(
                'div[@class="tags"]/a[@class="tag"]/text()').extract()
            yield QuoteItem(author=author, quote=quote, tags=tags)
            yield response.follow(
                url=self.start_urls[0] + text.xpath('span/a/@href').get(), callback=self.parse_author)

        next_link = response.xpath('/html//li[@class="next"]/a/@href').get()
        if next_link:
            next_url = self.start_urls[0] + next_link
            yield LinkItem(next_link=next_url)
            yield scrapy.Request(url=next_url)

    def parse_author(self, response):
        body = response.xpath('/html//div[@class="author-details"]')
        fullname = body.xpath('h3[@class="author-title"]/text()').get().strip()
        birth_date = body.xpath(
            'p/span[@class="author-born-date"]/text()').get().strip()
        birth_location = body.xpath(
            'p/span[@class="author-born-location"]/text()').get().strip()
        description = body.xpath(
            'div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(
            fullname=fullname, birth_date=birth_date, birth_location=birth_location, description=description)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Spider)
    process.start()
