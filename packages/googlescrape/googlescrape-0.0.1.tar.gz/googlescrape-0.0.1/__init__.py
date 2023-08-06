import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import re
from bs4 import BeautifulSoup

class GoogleScrapeException(Exception):
    pass
def take_screenshot(browser,url, save_fn="capture.png"):
    if not url.startswith('http://') and not url.startswith('https://'):
        url="https://"+url
    try:
        browser.get(url)
    except Exception as ex:
        if isinstance(ex,selenium.common.exceptions.WebDriverException):
            raise GoogleScrapeException("The url provided to take a screenshot was invalid!")
            return
        elif isinstance(ex,selenium.common.exceptions.InvalidSessionIdException):
            gChromeOptions = webdriver.ChromeOptions()
            gChromeOptions.add_argument("window-size=1080x1080")
            gChromeOptions.add_argument("--disable-dev-shm-usage")
            s=Service(ChromeDriverManager().install())
            browser = webdriver.Chrome(options=gChromeOptions,service=s)
            take_screenshot(url,save_fn)
            return
        else:
            raise ex
            return
    try:
        browser.save_screenshot(save_fn)
    except:
        raise GoogleScrapeException("The url requested didn't load up properly and crashed!")
        return
    f = open(save_fn, "r")
    my_file=f.read()
    f.close()
    return my_file
def removetags(raw_html):
  CLEANR = re.compile('<.*?>') 
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext
class Client:
    def __init__(self):
        gChromeOptions = webdriver.ChromeOptions()
        gChromeOptions.add_argument("window-size=1080x1080")
        gChromeOptions.add_argument("--disable-dev-shm-usage")
        s=Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(options=gChromeOptions,service=s)
        self.browser=browser
    def imagesearch(self,search):
        search=search.replace(" ","+")
        return take_screenshot(self.browser,f"https://www.google.com/search?q={search}")
    def textsearch(self,search):
        search=search.replace(" ","+")
        url=f"https://www.google.com/search?q={search}"
        html_doc=requests.get(url, 'html.parser').text
        soup = BeautifulSoup(html_doc, 'html.parser')
        resultstring=""
        resultstring=resultstring+removetags(str(soup.h1))
        listpara=soup.find_all('p')
        parastr=""
        for para in listpara:
            parastr=parastr+str(para)+"\n"
        resultstring=resultstring+removetags(parastr)
        return resultstring


