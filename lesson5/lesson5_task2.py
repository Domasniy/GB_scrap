from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
from pprint import pprint
import re

chrome_options = Options()
chrome_options.add_argument('start-maximized')
#убираем notification запросы в браузере
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(options = chrome_options)

driver.get('https://www.mvideo.ru/')

assert "М.Видео" in driver.title
#шелкаем на кнопу запроса города
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class*='btn-approve-city']"))).click()

#выбираем iframe всплывающего окна, и закрываем его
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it("fl-296415"))
WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-fl-track='click-button-close']"))).click()

#возвращаемся в главное окно и перемещаемся к клавише далее в блоке Хиты продаж
driver.switch_to.default_content()
hit_block_next_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Хиты продаж')]/../../..//a[contains(@class,'next-btn sel-hits-button-next')]")))
ActionChains(driver).move_to_element(hit_block_next_button).perform()

#шелкаем на далее пока у клавиши не появится атрибут disabled
while True:
    try:
        WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Хиты продаж')]/../../..//a[contains(@class,'next-btn sel-hits-button-next disabled')]")))
        break
    except:
        hit_block_next_button.click()
        time.sleep(1)
        
hit_products = driver.find_elements_by_xpath("//div[contains(text(),'Хиты продаж')]/../../..//a[@data-product-info]")


hit_info_list = []
for hit in hit_products:
    #Пришлось костыль делать, чтобы убрать инчи(двойные кавычки), а то словарь не делается :)
    hit_info_list.append(re.sub('(\d+\.\d)(\")', r"\1",hit.get_attribute('data-product-info').replace("\n",'').replace("\t",'') ))

pprint(hit_info_list)

