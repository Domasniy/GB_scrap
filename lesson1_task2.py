# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
import requests
import json

API_KEY = ''
URL = 'https://geekbrains.ru'
scan_if_not = 1
param = {'apikey' : API_KEY, 'resource' : URL, 'scan' : scan_if_not}

req = requests.get('https://www.virustotal.com/vtapi/v2/url/report',params=param)

data = req.json()
with open('scan_result.json', 'w') as outfile:
    json.dump(data, outfile)


print(f'Проверка {data["url"]}')
print(f'Результат вредоносов: обнаружено в {data["positives"]} базах из {data["total"]}')