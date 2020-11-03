import csv
from getpass import getpass
from selenium import webdriver
from time import sleep
import time
import json 
from os.path import isfile
from random import randrange
from bs4 import BeautifulSoup
import config
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector




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

'''
---------------------------------------------------------
This function writes to csv excel file 
---------------------------------------------------------
'''
def write_to_csv(filename,dict_array):
    myFile = open(filename, "w")
    with myFile:
        fieldnames = ['name', 'job description','location','infos','position','current company','school','mail','phone']
        writer = csv.DictWriter(myFile, fieldnames=fieldnames)
        writer.writeheader()
        for row in dict_array:
            writer.writerow(row)
'''
---------------------------------------------------------
This function validates field 
---------------------------------------------------------
'''
def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field
def validate_button(button):
    if button is None:
        return -1
    else:
        return button
'''
------------------------------------------------------------------------
           ASK FOR EMAIL AND PASSWORD
------------------------------------------------------------------------
'''
user_email =input("Enter Email:")
password =getpass()
print("Firefox Starting...")
sleep(randrange(5,7))
'''
------------------------------------------------------------------------
            SELENIUM DRIVER STARTS
------------------------------------------------------------------------
'''
cookies = get_saved_cookies()

options = {
    'connection_timeout': None  # Never timeout, otherwise it floods errors
}


driver = webdriver.Firefox(
    executable_path='/Users/user/Desktop/geckodriv/geckodriver', seleniumwire_options=options,
)
driver.header_overrides = config.headers

driver.get("https://www.linkedin.com/robots.txt")
for k, v in cookies.items():
    driver.add_cookie({'name': k, 'value': v})


driver.get("https://www.linkedin.com")
'''
------------------------------------------------------------------------
            SIGN IN
------------------------------------------------------------------------
'''
email_button = driver.find_element_by_xpath('//*[@id="session_key"]')
email_button.send_keys(user_email)
sleep(randrange(3,5))
pass_button = driver.find_element_by_xpath('//*[@id="session_password"]')
pass_button.send_keys(password)
sleep(randrange(3,5))
submit_button = driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/form/button')
submit_button.click()
print("Log in...")
'''
------------------------------------------------------------------------
            Go to google
------------------------------------------------------------------------
'''
#NONE
dict_array=[]

with open('Url.txt','r') as file:
   for line in file.readlines():

        driver.get(line)
        sleep(randrange(6,10))

        source_orig = driver.page_source


        name = ''
        Status = ''
        Infos = ''
        location = ''
        LastRole = ''
        LastRoleCompany = ''
        mail = ''
        phone = ''

        source_html = BeautifulSoup(source_orig, 'html.parser')


        name_elem = source_html.find('div', attrs={'class': 'flex-1 mr5'})
        if name_elem is not None:
            try:
                name = name_elem.find('li', attrs={'class': 'inline t-24 t-black t-normal break-words'}).text
            except:
                pass

        Status_elem = source_html.find('div', attrs={'class': 'flex-1 mr5'})
        if Status_elem is not None:
            try:
                Status = Status_elem.find('h2', attrs={'class': 'mt1 t-18 t-black t-normal break-words'}).text
            except:
                pass

        location_elem = source_html.find('div', attrs={'class': 'flex-1 mr5'})
        if location_elem is not None:
            try:
                location = location_elem.find('li', attrs={'class': 't-16 t-black t-normal inline-block'}).text
            except:
                pass

        sleep(randrange(3,6))
        driver.execute_script("scrollBy(0,800);")
        sleep(randrange(3,6))
        page = driver.find_element_by_tag_name('html')
        page.send_keys(Keys.END)
        sleep(randrange(4,6))

        source_orig = driver.page_source



        source_html = BeautifulSoup(source_orig, 'html.parser')

        Infos_elem = source_html.find('p', attrs={'class': 'pv-about__summary-text mt4 t-14 ember-view'})
        if Infos_elem is not None:
            try:
                Infos = Infos_elem.find('span', attrs={'class': 'lt-line-clamp__line'}).text
            except:
                pass

        LastRole_elem = source_html.find('div', attrs={'class': 'pv-entity__summary-info pv-entity__summary-info--background-section mb2'})
        if LastRole_elem is not None:
            try:
                LastRole = LastRole_elem.find('h3', attrs={'class': 't-16 t-black t-bold'}).text
            except:
                pass

        LastRoleCompany_elem = source_html.find('div', attrs={'class': 'pv-entity__summary-info pv-entity__summary-info--background-section mb2'})
        if LastRoleCompany_elem is not None:
            try:
                LastRoleCompany = LastRoleCompany_elem.find('p', attrs={'class': 'pv-entity__secondary-title t-14 t-black t-normal'}).text
            except:
                pass

        sleep(randrange(6,10))
        Url_two = line + 'detail/contact-info/'
        driver.get(Url_two)
        sleep(randrange(6,10))

        source_orig = driver.page_source

        source_html = BeautifulSoup(source_orig, 'html.parser')

        mail_elem = source_html.find('section', attrs={'class': 'pv-contact-info__contact-type ci-email'})
        if mail_elem is not None:
            try:
                mail = mail_elem.find('a', attrs={'class': 'pv-contact-info__contact-link link-without-visited-state t-14'}).text
            except:
                pass

        phone_elem = source_html.find('li', attrs={'class': 'pv-contact-info__ci-container t-14'})
        if phone_elem is not None:
            try:
                phone = phone_elem.find('span', attrs={'class': 't-14 t-black t-normal'}).text
            except:
                pass



        print(name)
        print(Status)
        print(location)
        print(Infos)
        print(LastRole)
        print(LastRoleCompany)
        print(mail)
        print(phone)
        if mail != '' or phone != '':
            dict_row={'name':name,'job description':Status,'location':location,'infos':Infos,'position':LastRole,'current company':LastRoleCompany,'mail':mail,'phone':phone}
            dict_array.append(dict_row)
            sleep(randrange(5, 10))
            write_to_csv("results.csv",dict_array)
            #dict_array.clear()

        else:
            print('Not load to the csv')
'''
------------------------------------------------------------------------
            Log out
------------------------------------------------------------------------
'''
driver.get('https://www.linkedin.com')
sleep(randrange(5,7))
try:
    nav_menu_button = driver.find_element_by_xpath("//*[@id='nav-settings__dropdown-trigger']")
    nav_menu_button.click()
except Exception:
    pass
sleep(randrange(5,7))
try:
    sign_out_button = driver.find_element_by_xpath("//a[@href='/m/logout/']")
    sign_out_button.click()
except Exception:
    pass
print("Log out...")
sleep(randrange(5,7))

print("Done...")
driver.close()
exit()
