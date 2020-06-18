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


emails = []
store_file = True # Сделать True, если нужно записать в файл
max_emails_enabled = True
max_emails = 10 # Ограничение на максимальное кол-во собранных писем
chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options = chrome_options)

driver.get('https://mail.ru')

assert "Mail.ru" in driver.title

#Заход в учетку
elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('')
elem.send_keys(Keys.RETURN)

elem = WebDriverWait(driver,5).until(
    EC.element_to_be_clickable((By.ID, 'mailbox:password'))
)
elem.send_keys('')
elem.send_keys(Keys.RETURN)

time.sleep(3)
#Парсинг первого письма
ActionChains(driver).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()
time.sleep(1)
email_from = driver.find_element_by_class_name('letter-contact').get_attribute('title')
email_date = driver.find_element_by_class_name('letter__date').text
email_subject = driver.find_element_by_class_name('thread__subject').text
email_body = driver.find_element_by_class_name('js-readmsg-msg').text
emails.append({'email_from': email_from, 'email_date': email_date, 'email_subject': email_subject, 'email_body': email_body})

#Парсинг последующих писем путем нажатия на CTRL-стрелка вниз
while True and (max_emails - 1) != 0:
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.DOWN).key_up(Keys.CONTROL).perform()
    time.sleep(1)
    email_from = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    email_date = driver.find_element_by_class_name('letter__date').text
    email_subject = driver.find_element_by_class_name('thread__subject').text
    email_body = driver.find_element_by_class_name('js-readmsg-msg').text.strip()
    emails.append({'email_from': email_from, 'email_date': email_date, 'email_subject': email_subject, 'email_body': email_body})
    if max_emails_enabled:
        max_emails -= 1
 #проверка что кнопка вниз на сайте имеет класс button2_disabled, который добавляется на посленем письма
 # Если класс есть, заканчиваем работу.   
    try:
        WebDriverWait(driver,1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[class*='button2_disabled']"))
        )
        break
    except:
        continue


# Сохранение в файл json собранных данных
if store_file:
    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(emails, outfile, ensure_ascii=False, indent=4)

pprint(emails)

driver.quit()

