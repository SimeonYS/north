import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import NorthItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class NorthSpider(scrapy.Spider):
	name = 'north'
	start_urls = ['https://www.northrim.com/About-Northrim/About-Us/Newsroom']

	def parse(self, response):
		articles = response.xpath('//div[@class="row wsc-margin-bottom-sm"]')
		for article in articles:
			date = article.xpath('.//div[@class="btn btn-medium btn-rounded btn-blog1"]/text()').get().strip() + '.' + article.xpath('.//span[@class="wsc_date"]/text()').get() + '.2021'
			post_links = article.xpath('.//div[@class="read_more"]/a/@href').get()
			yield response.follow(post_links, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h1[@class="post_link"]/text()').get()
		content = response.xpath('//div[@class="wsc_pi_body"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=NorthItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
