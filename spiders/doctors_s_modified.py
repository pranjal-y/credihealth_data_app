import csv
import scrapy
from scrapy.crawler import CrawlerProcess

class DoctorSpider(scrapy.Spider):
    name = 'doctors_spiders'

    def start_requests(self):
        with open('/Users/pranjalyadav/Downloads/doc_urls.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            urls = [row[0] for row in reader]

        alternative_urls = urls[1:40:2]

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

        rating = response.xpath("//div[@class='rating-star fs-13 color-666 margin-0']/text()").get()

        bio_element = response.xpath("//div[@id='default_description']/text()")
        bio = bio_element.get().strip() if bio_element else "NA"
        awards_element = response.xpath("//span[contains(text(), 'Awards')]")
        if awards_element:
            awards = awards_element.get().strip()
        else:
            awards = "NA"

        hospital_element = response.xpath("//select[@id='hospital_change_select']/option[@selected]/text()").get()

        department_link = response.xpath("//a[@class='color-555 no-decoration']")
        department = department_link.xpath("text()").get() or "NA"

        education_elements = response.xpath("//div[@id='headingOne']//p[@class='margin-0 fs-14 padding-b10 color-555']")
        education = [element.xpath("string()").get().strip() for element in education_elements]

        availability_element = response.xpath(".//div[@class='time-td display-inblock margin-l20 chat_bot_margin']")
        day = availability_element.xpath("span[@class='fw-500']/text()").get()
        availability = day.strip() if day else "NA"

        experience_element = response.xpath("//span[contains(@class, 'experince')]")
        experience = experience_element.xpath("string()").get().strip() if experience_element else "NA"

        fees_element = response.xpath(
            ".//span[@class='fw-500'][contains(text(), 'Consult fees')]/following-sibling::span")
        fees = fees_element.xpath("normalize-space(.)").get() if fees_element else "NA"

        yield {
            'Name': name.strip(),
            'Designation': designation,
            'Rating': rating.strip() if rating else "NA",
            'Departments': department,
            'Availability': availability,
            'Experience': experience,
            'Fees': fees,
            'Bio': bio.strip() if bio else "NA",
            'Awards': awards,
            'Hospital': hospital_element.strip() if hospital_element else "NA",
            'Education': education,

        }

def run_spider():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'doctor_all_info.csv',
        'LOG_LEVEL': 'DEBUG'  # Add this to set the log level to DEBUG
    })

    process.crawl(DoctorSpider)
    process.start()

if __name__ == '__main__':
    run_spider()