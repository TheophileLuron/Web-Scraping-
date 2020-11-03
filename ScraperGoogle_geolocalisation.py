from selenium import webdriver
from time import sleep
import time
from random import randrange
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from scraper_api import ScraperAPIClient



client = ScraperAPIClient('********************')
result = client.get(url = 'https://www.google.com/maps/contrib/113811103574182320069/reviews/@46.3276522,3.1595249,6z/data=!3m1!4b1!4m3!8m2!3m1!1e1', render=True).text
print("starting getting information from the web ...")  


start_urls = [client.scrapyGet(url = 'https://www.google.com/maps/contrib/113811103574182320069/reviews/@46.3276522,3.1595249,6z/data=!3m1!4b1!4m3!8m2!3m1!1e1', render=True)]
def parse(self, response):

    yield scrapy.Request(client.scrapyGet(url = 'https://www.google.com/maps/contrib/113811103574182320069/reviews/@46.3276522,3.1595249,6z/data=!3m1!4b1!4m3!8m2!3m1!1e1', render=True), self.parse)


soup = BeautifulSoup(result, 'html.parser')




    
Adresse_text = []


Adresse_source = soup.find('div', attrs={'class': 'section-review-subtitle section-review-subtitle-nowrap'})

if Adresse_source is not None:
    try:
        Adresse = Adresse_source.find('span', attrs={'jstcache':'395'})
        Adresse_text.append(Adresse.text)
    except:
        pass

print(Adresse_text)
