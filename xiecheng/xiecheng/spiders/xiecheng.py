# *_*coding:utf-8 *_*

import scrapy
from scrapy.spiders import CrawlSpider
from lxml import etree
import re

from xiecheng.items import *



class XieCheng(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['ctrip.com']

    start_urls = ['http://vacations.ctrip.com/tours/d-sanya-61']

    cookies={
'_RGUID':'57b3c7e6-dd74-49ce-9f12-d987e94f762b',

'_RSG':'Ed4TTR.npU5hOtJfVOsIy9',
'_RDG':'2838f3723329b123eb0f6e3930f0a8b80c',
'MKT_Pagesource':'PC',
' appFloatCnt':1,
'_ga':'GA1.2.1507252994.1534332853',
'_gid':'GA1.2.222197141.1534332853',
'manualclose':1,
' adscityen':'Hangzhou',
'Session':'smartlinkcode=U1535&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=',
'Union':'AllianceID=1315&SID=1535&OUID=',
'cticket':'22F54D19F3B0D1350121A47C6A6F818609908A737116A248B8388FB2B8AB758F',
'DUID':'u=739F615E2EE97487CDAF87241F867D9A100EE517D768140F743C43D16C1AF9D4&v=0',
'IsNonUser':'F',
'ticket_ctrip':'uoeOwviAJ6VQEgTNwLuTqSV9j/bS+aOP3Riia1P+kyQbgkQZsD2giWV9sKaMvssG2O6TEbXdrE7r16ztAX1bjBnzuwCr8a49nZp2Kr5IP2IxmyEO/6V80Bt38mECe2TkGLCdZyPLvuLR7KwEPvm9W2HC2ExgDO1hkwGawe94zpOqUMxr5MRdVVERc6StV2WE0YWv7l9DDXwFR6JavPJ/rjLBNcqp83L/CKsB4TMu6bY021p5xd5bsJY9ZGvGFQWqu2JCyMUsWbEtdyCbx6pVJZa3b5OzlWkPlYoHIVkDAZQh0FLS4Gt9RKj08v5dTjw3',
'CtripUserInfo':'VipGrade=0&UserName=&NoReadMessageCount=1&U=19736193E19AF73F86A56C8684627FB6A223555481A23D2E',
'AHeadUserInfo':'VipGrade=0&UserName=&NoReadMessageCount=1&U=19736193E19AF73F86A56C8684627FB6A223555481A23D2E',
'_xsrf':'2|869ececa|7e30db9e508c923da10a6f6f347e1f5a|1534336973',
'_gat':1,
'ASP.NET_SessionSvc':'MTAuOC4xODkuNTR8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTUyNjYxMTM1ODAwMA',
'ASP.NET_SessionId':'w15fkh0lnzaxddlyh2exkkek',
'StartCity_Pkg':'PkgStartCity=17',
'_abtest_userid':'f833017c-87e9-4a53-831a-2e397b99c460',
'Visitor':1,
'_bfa':'1.1534332848436.21wvyx.1.1534332848436.1534336981391.2.11',
'_bfs':1.5,
'_RF1':'124.160.17.98',
'Mkt_UnionRecord':'%5B%7B%22aid%22%3A%221315%22%2C%22timestamp%22%3A1534337115772%7D%5D',
' __zpspc':'9.1.1534337109.1534337115.2%234%7C%7C%7C%7C%7C%23',
' _jzqco':'%7C%7C%7C%7C1534337110437%7C1.1787000832.1534337109361.1534337109362.1534337115808.1534337109362.1534337115808.undefined.0.0.2.2',
'_bfi':'p1%3D104317%26p2%3D103045%26v1%3D11%26v2%3D10'


    }

    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,cookies=self.cookies,callback=self.page_num,meta=self.meta)

    def page_num(self,response):
        page_url = response.xpath('//div[@id="_pg"]/a/@href').extract()
        page_end = []
        for url in page_url:
            p_url = re.match('//vacations.ctrip.com/tours/d-sanya-61/p(\d+)', url)
            if p_url != None:
                page_end.append(int(p_url.group(1)))
        m_page = max(page_end)
        for page in range(1, m_page + 1):
            print("开始下载---第 %s 页" % page)
            page_url = self.start_urls[0] + '/p' + str(page) + '#_flta'
            yield scrapy.Request(url=page_url, callback=self.parse)

    def parse(self, response):
        detail_page_url=response.xpath('//h2[@class="product_title"]/a/@href').extract()

        for url in list(set(detail_page_url)):
            detail_url='http:' + url

            yield scrapy.Request(url=detail_url,callback=self.detail_parse)


    def detail_parse(self,response):
        item=XiechengItem()

        title_1="".join(response.xpath('//div[@class="detail_main_title"]/h2/text()').extract())
        title_2="".join(response.xpath('//div[@class="detail_summary"]/h1/text()').extract())

        price_1="".join(response.xpath('//li[@class="product_city"]/div[@class="link_wrap"][1]//text()').extract())
        price_2="".join(response.xpath('//div[@class="from_city_list city_scroll_wrap"]//text()').extract())

        if price_1:
            ss=price_1.replace(' ', '')
            tt=ss.replace("\n", "")
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































