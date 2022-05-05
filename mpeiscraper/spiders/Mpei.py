import scrapy
from scrapy.http import HtmlResponse
from mpeiscraper.items import MpeiscraperItem


class MpeiSpider(scrapy.Spider):
    name = 'Mpei'
    allowed_domains = ['mpei.ru']
    start_urls = ['https://mpei.ru/personal/Pages/list.aspx']
    position_map = {'Статус:': 'status', 'Должность:': 'position'}

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[@class="mpei-p-list-abc"]/a/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.parse_letter)

    def parse_letter(self, response: HtmlResponse):
        next_links = response.xpath('//div[@class="mpei-p-list-result"]/span/a/@href').extract()
        for next_link in next_links:
            yield response.follow(next_link, callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):
        person_links = response.xpath('//div[@class="mpei-p-list-result"]/ol/li/a/@href').extract()
        for link in person_links:
            yield response.follow(link, callback=self.parse_person)

    def parse_person(self, response: HtmlResponse):
        info = response.xpath('//div[@class="mpei-p-info-wrap"]')
        if not info:
            print(f"wrong html code at {response.url}")
            return

        positions_headers = info.xpath('//h2[@class="ms-rteElement-H2"]/text()').extract()
        if 'Сотрудник' not in positions_headers:
            return

        full_name = info.xpath('h1[@class="ms-rteElement-H1"]/strong/text()').get()
        surname, name, patronymic, *_ = full_name.split(' ')

        info_rows = info.xpath('p[not(@class)]')
        # parse common part
        common_part = info_rows[0]
        common_part_rows = common_part.xpath('em')
        common_part_len = len(common_part_rows)

        email = common_part_rows[0].xpath('a/text()').get()
        scientific_title = None
        if common_part_len > 2:
            scientific_title = common_part_rows[1].xpath('text()').get()

        degree = common_part_rows[common_part_len-1].xpath('text()').get()
        if not degree:
            return
        # parse other parts
        found = None
        for position_info in info_rows[1:]:
            parts = position_info.xpath('em')
            result_position = {}
            for part in parts:
                key = part.xpath("preceding-sibling::text()").extract()[-1].strip()
                if key in self.position_map.keys():
                    result_position[self.position_map[key]] = part.xpath("text()").get()
            if result_position['status'] == 'штатный сотрудник':
                found = result_position
                break

        if found:
            yield MpeiscraperItem(surname=surname,
                                  patronymic=patronymic,
                                  name=name,
                                  position=result_position['position'],
                                  url=response.url,
                                  email=email,
                                  scientific_title=scientific_title,
                                  science_degree=degree)
