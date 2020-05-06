import scrapy
from scrapy.selector import Selector
from yourProject.items import DmozItem
import json

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    # allowed_domains = ["dmoz.org"]


    firstItem = ["arts", "business", "computers", "games", "health", "home", "news", "recreation", "reference", "regional", "science", "shopping", "society", "sports", "kids_and_Teens"]

    baseUrl = "https://www.dmoz-odp.org/"
    baseUrl = "https://www.dmoz-odp.org/World/Chinese_Simplified/" # 简体中文

    start_urls = [
        # "https://www.dmoz-odp.org/Computers/Programming/Languages/Python/Books/",
        # "https://www.dmoz-odp.org/Computers/Programming/Languages/Python/Resources/"
        # "https://www.dmoz-odp.org/Arts/"
    ]

    for item in firstItem:
        start_urls.append(baseUrl+item.capitalize()+"/")

    with open('start_urls.json', 'w') as f:

        json.dump(start_urls, f)



    def parse(self, response):
        sel = Selector(response)
        # sites = sel.xpath('//div[@id="page"]')
        # sites = sel.xpath('//div[@id="subcategories-div"]')
        sites = sel.xpath('//div[@id="subcategories-div"]//div[@class="browse-node"]')

        items = []
        for site in sites:
            item = DmozItem()
            # item['name'] = site.xpath('div/section/aside/@class').extract()
            item['name'] = site.xpath('div/@class').extract()
            item['title'] = site.xpath('div[@class="browse-node"]/text()').extract()
            item['link'] = site.xpath('text()').extract()
            item['desc'] = site.xpath('normalize-space(div/text())').extract()
            title = item['title']
            link = item['link']
            desc = item['desc']
            items.append(item)
        return items



