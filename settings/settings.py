import json

with open('settings/settings.json', 'r', encoding='utf-8') as file:
  data = json.load(file)

LABLE = data['lable']
