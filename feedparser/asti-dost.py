import feedparser
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
import smtplib
from email.parser import Parser


f = feedparser.parse('http://www.asti.dost.gov.ph/job-opportunities?format=feed&type=rss')
#f = feedparser.parse('http://twitrss.me/twitter_user_to_rss/?user=intel')

print "Date now in UTC: "
print datetime.utcnow()

job_items = ""

for item in f.entries:
	
	publishedDate = parse(item.published)
	
	if publishedDate.day == datetime.utcnow().day and publishedDate.month == datetime.utcnow().month:
		#print item.published
		#print publishedDate
		#print item.title
		#print item.link
		job_items = job_items + item.title + "\n" + item.link + "\n\n"
	
if job_items != "":
	print job_items
	mail_content = Parser().parsestr('From: mail@localhost \n'
									'To: fredpedro.wspi@gmail.com\n'
									'Subject: Test\n'
									'\n'
									'%s' % job_items)

	server = smtplib.SMTP('smtp.sendgrid.net')
	server.login('scrapy', 'scrapy123')
	server.sendmail(mail_content['from'], mail_content['to'], mail_content.as_string())
	server.quit()