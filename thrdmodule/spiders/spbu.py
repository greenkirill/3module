import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractor import LinkExtractor
from ..items import SpbuItem
import re
from bs4 import BeautifulSoup as BS
import uuid
def response_to_text(response):
    soup = BS(response._get_body().decode("utf-8"), "html.parser")
    for child in soup.body.children:
        if child.name == 'script':
            child.decompose() 
    res = soup.body.get_text()
    res = re.sub(r"\W", " ", res)
    res = re.sub(r"\d", " ", res)
    res = re.sub(r"\s+", " ", res)
    return res


class SpbuSpider(CrawlSpider):
    name = "spbu"
    allowed_domains = ["spbu.ru","www.spbu.ru"]
    start_urls = ["https://spbu.ru/"]
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True,
            ),
            follow=True,
            callback="parse_items"
        )
    ]
    path = "./spbu_files/"
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_items(self, response):
        item = SpbuItem()
        item['url'] = response.url
        filename = str(uuid.uuid4())
        with open("%s%s.txt" % (self.path, filename), "w", encoding="utf-8") as rf:
            rf.write(response_to_text(response))
        item['f_n'] = filename
        return item
