# coding:utf-8

from scrapy.spiders import CrawlSpider, Request, Rule
from imdb.items import ImdbItem
from scrapy.linkextractors import LinkExtractor


class ImdbSpider(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['www.imdb.cn']
    rules = (
        Rule(LinkExtractor(allow=r"/title/tt\d+$"), callback="parse_imdb", follow=True),
    )

    def start_requests(self):
        for i in range(1, 20):
            url = "http://www.imdb.cn/nowplaying/" + str(i)
            yield Request(url=url, callback=self.parse)

    def parse_imdb(self, response):
        item = ImdbItem()
        try:
            item['video_title'] = "".join(response.xpath('//*[@class="fk-3"]/div[@class="hdd"]/h3/text()').extract())
            item['video_rating'] = "".join(
                response.xpath('//*[@class="fk-3"]/div[@class="hdd"]/span/i/text()').extract())
            content = response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li').extract()
            for i in range(0, len(content)):
                if "片名" in content[i]:
                    if i == 0:
                        item['video_name'] = "".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[1]/a/text()').extract())
                if "别名" in content[i]:
                    if i == 1:
                        item['video_alias'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[2]/a/text()').extract())
                if "导演" in content[i]:
                    if i == 1:
                        item['video_director'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[2]/a/text()').extract())
                    elif i == 2:
                        item['video_director'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[3]/a/text()').extract())
                if "主演" in content[i]:
                    if i == 2:
                        item['video_actor'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[3]/a/text()').extract())
                    if i == 3:
                        item['video_actor'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[4]/a/text()').extract())
                if "上映时间" in content[i]:
                    if i == 4:
                        item['video_year'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[5]/a[1]/text()').extract())
                        a = response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[5]/a').extract()
                        length = len(a) - 1
                        try:
                            item['video_color'] = "".join(
                                response.xpath(
                                    '//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[5]/a/text()').extract()[length])
                        except Exception as e:
                            item['video_color'] = ""
                        try:
                            type = "|".join(
                                response.xpath(
                                    '//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[5]/a/text()').extract()[1:length])
                            maohao = type.split("：")
                            if len(maohao) > 0:
                                item['video_type'] = maohao[0]
                            else:
                                item['video_type'] = ""
                        except Exception as e:
                            item['video_type'] = ""
                    if i == 5:
                        item['video_year'] = "".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[6]/a[1]/text()').extract())
                        a = response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[6]/a').extract()
                        length = len(a) - 1
                        try:
                            item['video_color'] = "".join(
                                response.xpath(
                                    '//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[6]/a/text()').extract()[length])
                        except Exception as e:
                            item['video_color'] = ""
                        try:
                            type = "|".join(
                                response.xpath(
                                    '//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[6]/a/text()').extract()[1:length])
                            maohao = type.split("：")
                            if len(maohao) > 0:
                                item['video_type'] = maohao[0]
                            else:
                                item['video_type'] = ""
                        except Exception as e:
                            item['video_type'] = ""

                if "国家" in content[i]:
                    if i == 5:
                        item['video_area'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[6]/a[1]/text()').extract())
                        item['video_voice'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[6]/a[2]/text()').extract())
                    if i == 6:
                        item['video_area'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[7]/a[1]/text()').extract())
                        item['video_voice'] = "|".join(
                            response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[7]/a[2]/text()').extract())
            item['video_length'] = "".join(
                response.xpath(
                    '//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[@class="nolink"]/text()').extract()).replace(
                "&nbsp", "")
            item['video_language'] = "".join(
                response.xpath('//*[@class="fk-3"]/div[@class="bdd clear"]/ul/li[@class="nolink"]/a/text()').extract())
            item['video_summary'] = "".join(
                response.xpath(
                    '//*[@class="fk-4 clear"]/div[@class="bdd clear"]/i/text()').extract()).lstrip().rstrip().replace(
                "<br>", "")
            item['video_url'] = response.url
            yield item
        except Exception as error:
            log(error)
