# *_*coding:utf-8 *_*

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

from xiecheng.items import XiechengItem


class Xiechengspider(CrawlSpider):
    name = 'crawl_xiecheng'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://vacations.ctrip.com/tours/d-sanya-61']

    rules = (
        Rule(LinkExtractor(allow='//vacations.ctrip.com/tours/d-sanya-61(.*?)',),),
        Rule(LinkExtractor(allow='//vacations.ctrip.com/freetravel(.*?)'),callback='parse_item')

    )

    def parse_item(self, response):
        item = XiechengItem()

        title_1 = "".join(response.xpath('//div[@class="detail_main_title"]/h2/text()').extract())
        title_2 = "".join(response.xpath('//div[@class="detail_summary"]/h1/text()').extract())

        price_1 = "".join(response.xpath('//li[@class="product_city"]/div[@class="link_wrap"][1]//text()').extract())
        price_2 = "".join(response.xpath('//div[@class="from_city_list city_scroll_wrap"]//text()').extract())

        if price_1:
            ss = price_1.replace(' ', '')
            tt = ss.replace("\n", "")
            item['price'] = tt
            item['url'] = response.url

            if title_1:
                t1 = title_1.replace(' ', '')
                t_1 = t1.replace("\n", "")
                item['title'] = t_1
            elif title_2:
                t2 = title_2.replace(' ', '')
                t_2 = t2.replace("\n", "")
                item['title'] = t_2

            else:
                item['title'] = ''
            yield item

        elif price_2:
            ss = price_2.replace(' ', '')
            tt = ss.replace("\n", "")
            item['price'] = tt
            item['url'] = response.url
            if title_1:
                t1 = title_1.replace(' ', '')
                t_1 = t1.replace("\n", "")
                item['title'] = t_1
            elif title_2:
                t2 = title_2.replace(' ', '')
                t_2 = t2.replace("\n", "")
                item['title'] = t_2

            else:
                item['title'] = ''
            yield item

        else:
            print("---------下载失败-----------")


