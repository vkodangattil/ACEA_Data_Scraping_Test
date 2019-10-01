import scrapy
import csv

class QuotesSpider(scrapy.Spider):
    name = "ACEA"

    def start_requests(self):
        urls = ['https://www.netce.com/learning.php?page=coursedetails&courseid=1444']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        with open("ohioNurse.html", 'wb') as f:
            f.write(response.body)
        title = response.css('h1::text').get(0)
        coreInfo = response.css('p::text')[0].get()
        coreInfoList = coreInfo.splitlines()
        courseNumber = coreInfoList[0].strip()
        price = coreInfoList[2].strip()
        hourPerCredit = coreInfoList[4].strip()
        categories = response.css('h2::text')
        categories = categories[1:]
        categories = categories.getall()
        categoryText = response.css('p::text').getall()
        boldText = response.css('strong::text').getall()
        missing = response.css('span::text').getall()
        indStateNursingApprov = ""
        for i in range(12, 24):
            indStateNursingApprov += missing[i]
        tableOfContents = response.css('span[class=chapter] a::text').extract()
        finalTOB = ""
        for i in tableOfContents:
            finalTOB += i + "\n"
        with open('ACEA_Test.csv', mode='w') as csv_file:
            categories.insert(0, 'Course Title')
            categories.insert(1, 'Course Number')
            categories.insert(2, 'Price')
            categories.insert(3, 'Hour/Credit')
            fieldnames = categories
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
            writer.writeheader()
            writer.writerow({'Course Title': title, 'Course Number': courseNumber, 'Price': price, 'Hour/Credit': hourPerCredit, fieldnames[4]: categoryText[4], fieldnames[5]: boldText[6], fieldnames[6]: categoryText[7], fieldnames[7]: missing[6] + missing[7], fieldnames[8]: missing[8] + missing[9] + missing[10] + missing[11], fieldnames[9]: indStateNursingApprov, fieldnames[10]: missing[24], fieldnames[11]: categoryText[8], fieldnames[12]: categoryText[9], fieldnames[13]: missing[25] + " " + categoryText[10], fieldnames[14]: categoryText[11], fieldnames[15]: missing[26], fieldnames[16]: categoryText[12], fieldnames[17]: missing[27], fieldnames[18]: categoryText[13], fieldnames[19]: categoryText[14] + categoryText[15], fieldnames[20]: categoryText[16], fieldnames[21]: finalTOB, fieldnames[22]: categoryText[17]})
            self.log('Wrote csv ACEA_Test.csv')
        self.log('Saved file Ohio.html')