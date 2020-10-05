from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# PATH=$PATH:/usr/local/bin/geckodriver
#PATH = "/usr/local/bin/geckodriver"
driver = webdriver.Firefox()

driver.get("https://techwithtim.net")
print(driver.title)

search = driver.find_element_by_name("s")
search.send_keys("test")
search.send_keys(Keys.RETURN)

#print(driver.page_source)

time.sleep(5)

driver.quit()