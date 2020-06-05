import requests
import json

repo = 'Microsoft'
req = requests.get(f'https://api.github.com/users/{repo}/repos')
data = req.json()
#Сохраняем данные в JSON файл
with open('repo.json', 'w') as outfile:
    json.dump(data, outfile)

for repo in data:
    print(f'Repo name: {repo["full_name"]}\nRepo Url: {repo["html_url"]}')
    print('-' * 10)