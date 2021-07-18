import re
import time
import json
from message import Message

from selenium import webdriver as wdrive
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options


class BackendAPI:
    def __init__(self):
        self.PATH = '/Users/weijiazhao/Desktop/chrome/chromedriver2'
        self.base_url = "https://www.amazon.com/"
        # self.option = wdrive.ChromeOptions()
        # self.option.add_argument('headless')
        self.driver = wdrive.Chrome(self.PATH)
        self.data = {}
    
    def open_link(self, link):
        self.driver.get(link)

    #track
    def find_price(self):
        price = self.driver.find_element_by_id("priceblock_ourprice")
        return price.text
    
    def find_name(self):
        name = self.driver.find_element_by_id("productTitle")
        new_name = name.text.split()
        real_name = new_name[0] + " " + new_name[1] + " " + new_name[2]
        return real_name

    def read_json(self,file):
        with open(file,'r') as js:
            jsdata = js.read()
        newdata = json.loads(jsdata)
        return newdata

    def dump_json(self,obj,file):
        with open(file,'w') as js:
            json.dump(obj,js,indent=4)

    def track_product(self,url, track_rate):
        if url == "":
            pass
        else:
            num = 1
            while(True):
                time.sleep(track_rate)
                self.driver.get(url)
                #update information to json file
                keys = "attempt" + "_" + str(num)
                currtime = str(time.ctime())
                
                obj = self.read_json('/Users/weijiazhao/Desktop/Python/projects/amazonScraper/track.json')
                
                obj[keys] = []
                obj[keys].append({
                    'product':self.find_name(),
                    'price':float(self.find_price()[1:]),
                    'time':currtime
                })
                
                self.dump_json(obj,'/Users/weijiazhao/Desktop/Python/projects/amazonScraper/track.json')

                
                realdata = self.read_json('/Users/weijiazhao/Desktop/Python/projects/amazonScraper/track.json')
                
                #compare prices to check if discount
                if realdata[keys][0]['price'] > realdata['attempt_1'][0]['price']:
                    discount = int(realdata[keys][0]['price'] / realdata['attempt_1'][0]['price'])
                    mail = Message()
                    mail.send_email(f"Congrats!", "\n", "Original Price: {realdata['attempt_1'][0]['price']}",
                    "\n", "Current Price: {realdata[keys][0]['price']}", "\n", "Discount Rate: {int(100-discount)}")
                    
                    adatas = self.read_json('/Users/weijiazhao/Desktop/Python/projects/amazonScraper/track.json')
                    
                if num >= 100:
                        with open('/Users/weijiazhao/Desktop/Python/projects/amazonScraper/track.json', 'w') as r:
                            jsdata = json.loads(r.read())
                            for i in jsdata:
                                del i
                            json.dump(jsdata, r, indent=4)
                    
                
                
                else:
                    print("Not yet, keep waiting")
                
                num+=1

 

        #search 
    def get_search_item(self,sitem):
        item = sitem
        return item

    def search_products(self,sitem, page):
        url = self.base_url
        item = self.get_search_item(sitem)
        self.driver.get(url)
        search_bar = self.driver.find_element_by_id("twotabsearchtextbox")
        search_bar.send_keys(item)
        search_bar.send_keys(Keys.ENTER)
        i = 1
        for j in range(page):
            #grid
            mainpage = WebDriverWait(self.driver,10).until(ec.visibility_of_element_located((By.CLASS_NAME, "s-main-slot.s-result-list.s-search-results.sg-row")))
            products = mainpage.find_elements_by_xpath('//div[@data-index]')
        #page
            page_num = WebDriverWait(mainpage,10).until(ec.visibility_of_element_located((By.CLASS_NAME, "a-section.a-spacing-none.a-padding-base")))
            

            for product in products:
                try:
                    price = product.find_element_by_class_name("a-price-whole") 
                    name = 0
                    try:
                        name = product.find_element_by_class_name("a-size-medium.a-color-base.a-text-normal")
                    except:
                        name = product.find_element_by_class_name("a-size-base-plus.a-color-base.a-text-normal")
                    
                    pre_link = product.find_element_by_class_name('a-link-normal.a-text-normal')
                    link = pre_link.get_attribute('href')
                    fraction = product.find_element_by_class_name("a-price-fraction")
                    
                    name = name.text
                    price = price.text + "." + fraction.text
                    
                    keys = 'product_' + str(i)
                    self.data[keys] = {
                    'product_name':name,
                    'price':float(re.sub("[^\d\.]", "", price)),
                    'link': link
                    }
                    i += 1
                    
                except Exception as e:
                    print(f"error product {i}, problem: {e}")
                    i+=1
                    
            page = WebDriverWait(page_num, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'a-last')))
            page.click()
        
        self.dump_json(self.data,'/Users/weijiazhao/Desktop/Python/projects/amazonScraper/search.json')
        

 
if __name__ == '__main__':
    start = BackendAPI()
    start.search_products('mechanical keyboard', 1)