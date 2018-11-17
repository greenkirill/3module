import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import ThrdmoduleItem

TEXTRACT_EXTENSIONS = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".pptx", ".ppt", ".rar", ".jpeg", ".jpg", ""]

class CustomLinkExtractor(LinkExtractor):
    def __init__(self, *args, **kwargs):
        super(CustomLinkExtractor, self).__init__(*args, **kwargs)
        # Keep the default values in "deny_extensions" *except* for those types we want.
        self.deny_extensions = [ext for ext in self.deny_extensions if ext not in TEXTRACT_EXTENSIONS]


class SpbuOldSpider(CrawlSpider):
    # The name of the spider
    name = "spbu_old"

    # The domains that are allowed (links to other domains are skipped)
    # allowed_domains = ["127.0.0.1"]
    allowed_domains = ["spbu.ru","www.spbu.ru"]


    # The URLs to start with
    # start_urls = ["http://127.0.0.1/blekanov/site/root/index.html"]
    start_urls = ["https://spbu.ru/"]


    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            CustomLinkExtractor(
                canonicalize=True,
                unique=True,
                # deny=("http://127.0.0.1/blekanov/site/branch/*",
                #       r'^http:\/\/127\.0\.0\.1\/[^blekanov].*')
            ),
            follow=True,
            callback="parse_items"
        ),
        Rule(LinkExtractor(deny_extensions=set(), tags=('img',), attrs=('src',),canonicalize = True, unique = True), follow = False, callback='parse_image_link')

    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse_items(self, response):
        # The list of items that are found on the particular page
        items = []

        item_status = ThrdmoduleItem()
        item_status['record_type'] = 0
        item_status['url_from'] = response.url
        item_status['url_status'] = response.status
        items.append(item_status)

        if response.status in [404, 403]:
            return items

        # Only extract canonicalized and unique links (with respect to the current page)
        links = CustomLinkExtractor(canonicalize=True, unique=False).extract_links(response)
        # Now go through all the found links
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = True

            # for allowed_domain in self.allowed_domains:
            #     if allowed_domain in link.url:
            #         is_allowed = True

            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed:
                item = ThrdmoduleItem()
                item['record_type'] = 1
                item['url_from'] = response.url
                item['url_to'] = link.url
                item['url_status'] = response.status
                items.append(item)
        # Return all the found items
        return items

    def parse_image_link(self, response):
        item = ThrdmoduleItem()
        item['record_type'] = 2
        item['url_to'] = response.url
        item['url_from'] = response.request.headers.get('Referer', None)
        item['url_status'] = response.status
        yield item