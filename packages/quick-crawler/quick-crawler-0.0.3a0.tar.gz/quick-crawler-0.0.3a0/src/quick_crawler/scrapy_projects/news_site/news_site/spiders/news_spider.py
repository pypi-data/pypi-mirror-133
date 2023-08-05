import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider
from quick_crawler import page
import os
MAX_NUM_URLS=1000
url_count=0

def get_page_meta(html_str):
    soup = BeautifulSoup(html_str, features="lxml")

    keywords=""
    description=""

    title = soup.title.string
    print('title = ', title)

    # print(soup.attrs)
    html=soup.find("html")
    if "lang" in html.attrs.keys():
        lang = html["lang"]
    else:
        lang = ""
    print("lang = ",lang)

    meta = soup.find_all('meta')
    # print(html_str)
    for tag in meta:
        if 'name' in tag.attrs.keys():
            name=tag.attrs['name'].strip().lower()
            if name=="description":
                description=tag.attrs['content']
            if name=="keywords":
                keywords=tag.attrs['content']
    model = {
        "title":title.replace("\n",""),
        "lang":lang,
        "keywords":keywords.replace("\n",""),
        "description":description.replace("\n","")
    }
    return model

class NewsSpider(CrawlSpider):
    name = 'CNN'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        global url_count
        global list_model
        url_count+=1
        print(self.name + "'s URL: ", response.url)
        html_str=response.text
        meta_model=get_page_meta(html_str)
        meta_model["url"]=page.quick_remove_unicode(response.url)
        meta_model["id"]=page.quick_remove_unicode(self.name)
        print(meta_model)
        #list_model.append(meta_model)
        if url_count>=MAX_NUM_URLS:

            raise CloseSpider('termination condition met')
        return meta_model


