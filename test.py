import urllib
from selenium import webdriver as wdrive

PATH = '/Users/weijiazhao/Desktop/chrome/chromedriver2'
base_url = "https://www.amazon.com/"
driver = wdrive.Chrome(PATH)

driver.get('https://www.amazon.com/s?k=curtain+rod&ref=nb_sb_noss_1')

# get the image source
img = driver.find_elements_by_tag_name('img')
for i in img:
    image = i.get_attribute("src")
    print(image)

driver.close()