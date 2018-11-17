import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractor import LinkExtractor
from ..items import TgrItem
import re
from bs4 import BeautifulSoup as BS

def ret_item(response):
    item_status = TgrItem()
    item_status['url'] = response.url
    soup = BS(response._get_body().decode("utf-8"), "html.parser")
    for child in soup.body.children:
        if child.name == 'script':
            child.decompose() 
    res = soup.body.get_text()
    res = re.sub(r"\W", " ", res)
    res = re.sub(r"\d", " ", res)
    res = re.sub(r"\s+", " ", res)
    item_status['content'] = res
    with open("123.txt", "w", encoding="utf-8") as rf:
        rf.write(res)
    return item_status


# class CustomLinkExtractor(LinkExtractor):
#     def __init__(self, *args, **kwargs):
#         super(CustomLinkExtractor, self).__init__(*args, **kwargs)
#         # Keep the default values in "deny_extensions" *except* for those types we want.
#         self.deny_extensions = [ext for ext in self.deny_extensions if ext not in TEXTRACT_EXTENSIONS]


class TgrSpider(CrawlSpider):
    name = "tgr"
    allowed_domains = ["tgr.am","ru.tgr.am"]
    start_urls = ["https://tgr.am/"]
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
    itr = 0
    path = "./fls/"
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_items(self, response):
        item_status = TgrItem()
        item_status['url'] = response.url
        soup = BS(response._get_body().decode("utf-8"), "html.parser")
        for child in soup.body.children:
            if child.name == 'script':
                child.decompose() 
        res = soup.body.get_text()
        res = re.sub(r"\W", " ", res)
        res = re.sub(r"\d", " ", res)
        res = re.sub(r"\s+", " ", res)
        with open("%s%i.txt" % (self.path, self.itr), "w", encoding="utf-8") as rf:
            rf.write(res)
        item_status['f'] = self.itr
        self.itr += 1
        return item_status