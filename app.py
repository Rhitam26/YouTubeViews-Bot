config_file = "config.json"
log_f = 'logs.log'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import threading
import time
import logging, json
import pandas as pd
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display


# Define your proxy information
proxy_host = 'geo.iproyal.com'
proxy_port = '12321'
proxy_username = 'Anukul026'
proxy_password = 'Happy8980'

# Create a thread-local storage for WebDriver instances
thread_local = threading.local()


logging.basicConfig(filename=log_f, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info("---------------------Starting the script-----------------------")

class cnt_Que:
    def __init__(self):
        self.success_items = []
        self.failed_items = []
        self.failed_urls =[]
        self.passed_urls =[]
    def enque_s(self, url):
        # check if url is present in as one of the keys in the list of dicts
        if url in [d['url'] for d in self.success_items]:
            # increase the count by 1
            for d in self.success_items:
                if d['url'] == url:
                    d['count'] += 1
        else:
            self.success_items.append({'url':url, 'count':1})
        
    def enque_f(self, url):
        if url in [d['url'] for d in self.failed_items]:
            # increase the count by 1
            for d in self.failed_items:
                if d['url'] == url:
                    d['count'] += 1
        else:
            self.failed_items.append({'url':url, 'count':1})
    def len_success(self):
        return len(self.success_items)
    def len_failed(self):
        return len(self.failed_items)
    
    def print_success(self):
        str = ""
        for d in self.success_items:
            str += f"{d['url']} : {d['count']}\n"
        return str
    
    def print_failed(self):
        str = ""
        for d in self.failed_items:
            str += f"{d['url']} : {d['count']}\n"
        return str
    
global queue
queue= cnt_Que()

     
def get_driver():
    try:
        if not hasattr(thread_local, "driver"):
            chrome_options = Options()
            # chrome_options.add_argument('--proxy-server={}:{}'.format(proxy_host, proxy_port))
            proxy = f"{proxy_host}:{proxy_port}"
            chrome_options.add_argument(f'--proxy-server={proxy}')
            chrome_options.add_argument(f'--proxy-auth={proxy_username}:{proxy_password}')
            # chrome_options.add_argument("_incognito")
            thread_local.driver = webdriver.Chrome(executable_path=r"C:\Users\neevd\MyDen\Projects\YouTubeLikes_ProxyIPs\Driver\chromedriver-win64\chromedriver.exe", options=chrome_options)
            logging.info("Driver created")
        return thread_local.driver
    except Exception as e:
        logging.error(f"Exception occured while creating driver {e}")
        return None

def scrape_using_driver(url):
    try:
        logging.info("Starting scrape_using_driver for url: "+url)
        driver = get_driver()
        # Your scraping logic here
        # url = 'https://www.youtube.com/shorts/FynQv0R4d5w'
        driver.get(url)
        # wait for page to load
        # driver.implicitly_wait(10)
        # print("Exception Occured")
        
        driver.implicitly_wait(5)
        setting = driver.find_element(By.CLASS_NAME, 'ytp-settings-button')
        setting.click()
        # Click quality button
        driver.implicitly_wait(5)
        quality = driver.find_element(By.XPATH, '//div[@class="ytp-menuitem"]/div[text()="Quality"]')
        quality.click()
        # Click 720p
        time.sleep(0.5)
        res = driver.find_element(By.XPATH, '//span[text()="144p"]')
        res.click()
        driver.find_element("id","content").click()
        # wait for 10 seconds
        time.sleep(8)
        queue.enque_s(url)
        logging.info("Video completed for url: "+url)
    except Exception as e:
        logging.error(f"Exception occured while watching {url} for reason   {e}")
        queue.enque_f(url)

    

# read the input file
df = pd.read_excel("./Input/video_list.xlsx")
logging.info("Input file read successfully")


for index, row in df.iterrows():
    url = row['URLs']
    views = row['Views']
    threads = []
    for _ in range(views):
        
        t = threading.Thread(target=scrape_using_driver, args=(url,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
        if len(threads) ==7:
                for t in threads:
                    t.join()  
                threads.clear()

    for t in threads:
        t.join()

logging.info("All threads completed")
logging.info("Success items: "+queue.print_success())
logging.info("Failed items: "+queue.print_failed())
logging.info("Total Success items: "+str(queue.len_success()))
logging.info("Total Failed items: "+str(queue.len_failed()))
logging.info("---------------------Ending the script-----------------------")
# Quit all WebDriver instances



