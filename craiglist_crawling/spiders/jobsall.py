import scrapy
import time 
from scrapy import Request
from scrapy.utils.markup import remove_tags

class JobsallSpider(scrapy.Spider):
    name = "jobsall"
    allowed_domains = ["craigslist.org"]
    start_urls = ["https://newyork.craigslist.org/search/egr"]
    custom_settings = {'FEED_EXPORT_FIELDS' :['Extract_Date','PostID','Post_Date','Title','URL','Address','Compensation','Employment Type','Description']}

    # open and delete all the content & write "data=" in data.json file after each crawl
    datafile = open('data.json', 'w')
    datafile.write('data=')
    datafile.close()

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')
        extract_date = time.strftime("%x - %X")

        for job in jobs:
            post_date = job.xpath('//p[@class="result-info"]/time/@datetime').extract_first()
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]

            yield Request(absolute_url, callback=self.parse_page, meta={'Extract_Date':extract_date,'Post_Date': post_date, 'URL': absolute_url, 'Title': title, 'Address':address})

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = "https://newyork.craigslist.org" + relative_next_url

        yield Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        post_date = response.meta.get('Post_Date')
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
        extract_date = response.meta.get('Extract_Date')


        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())

        compensation = response.xpath('//p[@class="attrgroup"]/span[1]/b/text()').extract_first()
        employment_type = response.xpath('//p[@class="attrgroup"]/span[2]/b/text()').extract_first()
        postID = response.xpath('//div[@class="postinginfos"]/p[1]/text()').extract_first("")[9:]

        yield{'Extract_Date':extract_date,'PostID':postID,'Post_Date': post_date, 'URL': url, 'Title': title, 'Address':address, 'Compensation':compensation, 'Employment Type':employment_type,'Description':description}
        
    