import csv
import scrapy
from scrapy.crawler import CrawlerProcess

class DoctorSpider(scrapy.Spider):
    name = 'doctors_spiders'

    def start_requests(self):
        with open('/Users/pranjalyadav/Downloads/doc_urls.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            urls = [row[0] for row in reader]

        alternative_urls = urls[1::2]

        for url in alternative_urls:
            self.logger.debug("Processing URL: %s", url)
            yield scrapy.Request(url=url, callback=self.parse_doctor)

    def parse_doctor(self, response):
        self.logger.debug("Processing URL: %s", response.url)

        name = response.xpath("//a[@class='color-inherit no-decoration']/text()").get() or "NA"
        designation_element = response.xpath("//p[@class='margin-0 margin-b10']/text()")
        if designation_element:
            designation = designation_element.get()
            designation = designation.strip()
            if not designation.strip():
                designation = "Consultant"
        else:
            designation = "Consultant"
        department_link = response.xpath("//a[@class='color-555 no-decoration']")
        department = department_link.xpath("text()").get() or "NA"

        availability_element = response.xpath(".//div[@class='time-td display-inblock margin-l20 chat_bot_margin']")
        day = availability_element.xpath("span[@class='fw-500']/text()").get()
        availability = day.strip() if day else "NA"

        experience_element = response.xpath("//span[@class='experince margin-r10 float-left']/text()")
        experience = experience_element.get() or "NA"

        fees_element = response.xpath(
            ".//span[@class='fw-500'][contains(text(), 'Consult fees')]/following-sibling::span")
        fees = fees_element.xpath("normalize-space(.)").get() if fees_element else "NA"

        yield {
            'Name': name.strip(),
            'Designation': designation,
            'Department': department,
            'Availability': availability,
            'Experience': experience.strip(),
            'Fees' : fees
        }

def run_spider():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'doctor_details.csv',
        'LOG_LEVEL': 'DEBUG'  # Add this to set the log level to DEBUG
    })

    process.crawl(DoctorSpider)
    process.start()

if __name__ == '__main__':
    run_spider()





