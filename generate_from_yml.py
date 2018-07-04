import sys
import yaml
import json

yaml_file = open('src/categories-coded.yml', 'r')
categories_dict = yaml.load(yaml_file)

category_codes = set([c['code'] for c in categories_dict['categories']])


if len(categories_dict['categories']) != len(category_codes):
	sys.exit("Error! Category codes need to be unique!")

category_codes_tokenized = [c.split('-') for c in category_codes]

for category_tokens in category_codes_tokenized:
	parent_tokens = category_tokens[0:(len(category_tokens)-2)]
	if parent_tokens:
		if parent_tokens not in category_codes_tokenized:
			category_code = '-'.join(category_tokens)
			sys.exit("Error! " + category_code + " does not map to a parent category!")

with open('dist/categories-coded.json', 'w', encoding='utf-8') as json_file:
	json.dump(categories_dict, json_file, indent=4, ensure_ascii=False)
