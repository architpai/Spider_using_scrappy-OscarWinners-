import scrapy
import time

# creating a single spider with name oscars
class OscarsSpider(scrapy.Spider):
    name = "oscars"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"]

    def parse(self, response):
        for href in response.css(r"tr[style='background:#FAEB86'] a[href*='film)']::attr(href)").extract():
            url = response.urljoin(href)
            print(url)
            req = scrapy.Request(url, callback=self.parse_titles)
            time.sleep(5)
            yield req

    def parse_titles(self, response):
        for sel in response.css('html').extract():
            data = {}
            data['title'] = response.css(r"h1[id='firstHeading'] i::text").extract()
            data['director'] = response.css(r"tr:contains('Directed by') a[href*='/wiki/']::text").extract()
            data['starring'] = response.css(r"tr:contains('Starring') a[href*='/wiki/']::text").extract()
            data['releasedate'] = response.css(r"tr:contains('Release date') li::text").extract()
            data['runtime'] = response.css(r"tr:contains('Running time') td::text").extract()
        yield data

# to run - scrapy crawl oscars -o oscars.csv