import sys
import yaml
import json

yaml_file = open('src/categories-coded.yml', 'r')
categories_dict = yaml.load(yaml_file)

print("Checking category tree format.")

category_codes = set([c['code'] for c in categories_dict['categories']])

if len(categories_dict['categories']) != len(category_codes):
	sys.exit("Error! Category codes need to be unique!")

for category_code in category_codes:
	last_hyphen_position = category_code.rfind("-")

	if last_hyphen_position == -1:
		continue

	parent_code = category_code[0:last_hyphen_position]

	#print(category_code, parent_code)

	if parent_code not in category_codes:
		sys.exit("Error! " + category_code + " does not map to a parent category!")

print("Category tree is in correct format! Exporting YAML to JSON.")

with open('dist/categories-coded.json', 'w', encoding='utf-8') as json_file:
	json.dump(categories_dict, json_file, indent=4, ensure_ascii=False)

print("Export completed!")
