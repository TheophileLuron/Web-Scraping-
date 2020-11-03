import csv
from getpass import getpass
from selenium import webdriver
from time import sleep
import time
import json
from random import randrange
from bs4 import BeautifulSoup
import config
from os.path import isfile
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector



user_email = '***********'
password = '***********'

def get_saved_cookies():
    ''' returns cookie cache if exists '''
    if isfile(config.data_path):
        try:
            with open(config.data_path, 'r') as f:
                out = json.loads(f.read())
                cookies = out["cookies"]
                print("[+] Detected stored cookies, checking it")
                return cookies
        except Exception:
            print("[-] Stored cookies are corrupted")
            return False
    print("[-] No stored cookies found")
    return False

cookies = get_saved_cookies()

options = {
    'connection_timeout': None  # Never timeout, otherwise it floods errors
}


driver = webdriver.Firefox(
    executable_path='/Users/user/Desktop/geckodriv/geckodriver', seleniumwire_options=options,
)
driver.header_overrides = config.headers

driver.get("https://www.facebook.com/robots.txt")
for k, v in cookies.items():
    driver.add_cookie({'name': k, 'value': v})

sleep(randrange(5,7))

print("Webdriver Starting...")
driver.get("https://mtouch.facebook.com/login/")

sleep(randrange(5,7))
'''
------------------------------------------------------------------------
            SIGN IN
------------------------------------------------------------------------
'''
email_button = driver.find_element_by_xpath('//*[@id="m_login_email"]')
email_button.send_keys(user_email)
sleep(randrange(3,5))
pass_button = driver.find_element_by_xpath('//*[@id="m_login_password"]')
pass_button.send_keys(password)
sleep(randrange(3,5))
submit_button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/div[3]/form/div[5]/div[1]/button') 
submit_button.click()
print("Log in...")
