import scrapy
import logging

from scrapejobs.items import ScrapejobsItem
from scrapy.mail import MailSender

class  ScrapejobsSpider(scrapy.Spider):
	name = "dost"
	allowed_domains = ["dost.gov.ph"]
	start_urls = [
		"http://dost.gov.ph/transparency/admin-and-finance/job-opportunities/"
	]
	
	
	def parse(self, response):
		logging.basicConfig(filename='scraper.log', level=logging.DEBUG)
		mailer = MailSender(smtphost="smtp.sendgrid.net", mailfrom="scrapy@localhost",smtpuser="scrapy", smtppass="scrapy123", smtpport=25)
		
		job_item = []
		email_body = "DOST \n"
		for sel in response.xpath('//div[@id="jg_el_listing_single"]/table/tr[@style]'): #define jobs postigns table selector		
			item = ScrapejobsItem()
			item['title'] = sel.xpath('td[@class="jg_jobtitle"]/strong/text()').extract()
			item['link'] = sel.xpath('@onclick').extract()
			removed_prefix = ("".join(item['link'])).strip("window.location=")
			stripped_link = removed_prefix.strip("'")
			job_item.append("Job Item: " + "".join(item['title']) + "\n Link: http://dost.gov.ph" + stripped_link)

			#yield item

		for job in job_item:
			email_body = email_body + job + "\n\n"
		
		print email_body

		mailer.send(to=["fredpedro.wspi@gmail.com"], subject="Scrapy Job", body=email_body)