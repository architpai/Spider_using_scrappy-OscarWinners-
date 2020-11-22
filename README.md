# Introduction 
Scrapy uses spiders, which are self-contained crawlers that are given a set of instructions.
The goal of the project is to compile a list of the Oscar winners for best picture, along with their director, starring actors, release date, and run time. Using Google, we can see there are several sites that will list these movies by name, and maybe some additional information, but generally we’ll have to follow through with links to capture all the information you want.
Obviously, it would be impractical and time-consuming to go through every link from 1927 through to today and manually try to find the information through each page. With web scraping, we just need to find a website with pages that have all this information, and then point our program in the right direction with the right instructions.
we will use Wikipedia as our website as it contains all the information we need and then use Scrapy on Python as a tool to scrape our information.
## Importance of robots.txt
Data scraping involves increasing the server load for the site that you’re scraping, which means a higher cost for the companies hosting the site and a lower quality experience for other users of that site. The quality of the server that is running the website, the amount of data you’re trying to obtain, and the rate at which you’re sending requests to the server will moderate the effect you have on the server. 
Most sites also have a file called robots.txt in their main directory. This file sets out rules for what directories sites do not want scrapers to access. A website’s Terms & Conditions page will usually let you know what their policy on data scraping is.Disobeying a websites policy may result in site wide IP ban or other similar actions by the website to protect themseleves.
## The Setup:
Any good scrape job start with inspecting the website to be scraped and gather some metainformation about it like how the site is structed and whether data to be extarcted can be easily accessed using classes or id , or a rather rudimentary upproach might be required.I prefer to use the inbuilt ChromeDevTools 
for example o the wikipedia site all oscar winning movies have yellow color like so:

![](https://github.com/architpai/Spider_using_scrappy-OscarWinners-/blob/main/Screenshots/1.png)
 
Inside the spider is a class that you define that tells Scrapy what to do.
```
class OscarsSpider(scrapy.Spider):
   name = "oscars"
   allowed_domains = ["en.wikipedia.org"]
   start_urls = ["https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"]
```
The above class names the spider and gives it guidelines as to the what url to start on and what domains it can crawl.
Next we want to create a timer to restrict how fast the bot scrapes. Also, when we parse the pages the first time, we want to only get a list of the links to each title, so we can grab information off those pages instead.Below funtion acheives exactly that:

```
def parse(self, response):
   for href in response.css(r"tr[style='background:#FAEB86'] a[href*='film)']::attr(href)").extract():
       url = response.urljoin(href)
       print(url)
       req = scrapy.Request(url, callback=self.parse_titles)
       time.sleep(5)
       yield req
```
Here we make a loop to look for every link on the page that ends in film) with the yellow background in it and then we join those links together into a list of URLs, which we will send to the function parse_titles to pass further. We also slip in a timer for it to only request pages every 5 seconds.
```
def parse_titles(self, response):
   for sel in response.css('html').extract():
       data = {}
       data['title'] = response.css(r"h1[id='firstHeading'] i::text").extract()
       data['director'] = response.css(r"tr:contains('Directed by') a[href*='/wiki/']::text").extract()
       data['starring'] = response.css(r"tr:contains('Starring') a[href*='/wiki/']::text").extract()
       data['releasedate'] = response.css(r"tr:contains('Release date') li::text").extract()
       data['runtime'] = response.css(r"tr:contains('Running time') td::text").extract()
   yield data
```
The real work gets done in our parse_data function, where we create a dictionary called data and then fill each key with the information we want. Again, all these selectors were found using Chrome DevTools.
After all this is done we cd into our spiders folder and run in the terminal
```scrapy crawl oscars -o oscars.csv```

   
