import yaml
import json

yaml_file = open('categories-coded.yml', 'r')
categories_dict = yaml.load(yaml_file)

with open('categories-coded.json', 'w', encoding='utf-8') as json_file:
	json.dump(categories_dict, json_file, ensure_ascii=False)
