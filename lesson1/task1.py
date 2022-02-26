# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

username = 'SAMSI-RandTensors'

url = f'https://api.github.com/users/{username}/repos'

resp = requests.get(url)
repos = resp.json()

names = list(map(lambda repo: repo['name'], repos))
pprint(f'Repositories loaded: {names}')

with open('task1-out.json', 'w') as outfile:
    outfile.write(json.dumps(repos, indent=4))
