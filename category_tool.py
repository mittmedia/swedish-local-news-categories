import os
import random
import re
import string
from dataclasses import dataclass
from enum import Enum

import yaml


class ModAction(Enum):
    ADD = 1
    UPDATE = 2
    MOVE = 3
    INACTIVATE = 4


class CategoryStatus(Enum):
    ACTIVE = 1
    INACTIVE = 2
    REPLACED = 3


@dataclass
class Category:
    code: str
    level: int
    name: str
    status: CategoryStatus = CategoryStatus.ACTIVE
    description: str = ''
    replaces: str = None
    replacedBy: str = None


@dataclass
class ModOperation:
    action: ModAction
    code: str = None
    description: str = None
    name: str = None
    newName: str = None
    newParentCode: str = None
    newParentName: str = None
    parentName: str = None
    parentCode: str = None


def generate_new_code(parent_code, existing_codes):
    while True:
        sub_code = ""

        for _ in range(3):
            sub_code += random.choice(string.ascii_uppercase)

        new_code = parent_code + '-' + sub_code
        if new_code not in existing_codes:
            break

    return new_code


version = None

mod_file_path = 'src/mods'


def calculate_level(category_code):
    return len(category_code.split('-')) - 1


def load_categories():
    global version
    with open('src/categories-coded.yml', 'r', encoding='utf-8') as categories_file:
        categories_dict = yaml.load(categories_file)

    categories = {}

    for category in categories_dict['categories']:
        cat = Category(code=category['code'], level=category['level'], name=category['name'])

        if 'description' in category:
            cat.description = category['description']
        if 'replaces' in category:
            cat.replaces = category['replaces']
        if 'replacedBy' in category:
            cat.replacedBy = category['replacedBy']
        if 'status' in category:
            cat.status = category['status']

        categories[(cat.code, cat.name)] = cat

    version = categories_dict['version']

    return categories


def load_modification_files():
    global mod_file_path
    modifications = []
    for file_name in os.listdir(mod_file_path):
        if re.match("\d{14}.+.yml", file_name):
            modifications.extend(load_modification_file(file_name))

    return modifications


def load_modification_file(path):
    global mod_file_path
    file_path = mod_file_path + '/' + path
    with open(file_path, 'r', encoding='utf-8') as modification_file:
        mod_dict = yaml.load(modification_file)

    modifications = []

    print(file_path)

    for modification in mod_dict['modifications']:
        mod = ModOperation(action=ModAction[modification['action']])

        if 'code' in modification:
            mod.code = modification['code']
        if 'description' in modification:
            mod.replacedBy = modification['description']
        if 'name' in modification:
            mod.name = modification['name']
        if 'newName' in modification:
            mod.newName = modification['newName']
        if 'newParentCode' in modification:
            mod.newParentCode = modification['newParentCode']
        if 'newParentName' in modification:
            mod.newParentName = modification['newParentName']
        if 'parentCode' in modification:
            mod.parentCode = modification['parentCode']
        if 'parentName' in modification:
            mod.parentName = modification['parentName']

        modifications.append(mod)

    return modifications


def save_categories(categories):
    global version
    categories_output = {'categories': [], 'version': version}

    for key, value in categories.items():
        category = {'code': value.code, 'level': value.level, 'name': value.name, 'status': value.status.name}

        if value.description is not None:
            category['description'] = value.description

        if value.replaces is not None:
            category['replaces'] = value.replaces

        if value.replacedBy is not None:
            category['replacedBy'] = value.replacedBy

        categories_output['categories'].append(category)

    categories_output['categories'] = sorted(categories_output['categories'], key=lambda k: (k['code'], k['level']))

    with open('src/categories-coded.yml', 'w', encoding='utf-8', newline="\n") as categories_file:
        yaml.dump(categories_output, categories_file, default_flow_style=False, allow_unicode=True,
                  explicit_start=False,
                  width=4096, line_break="\n")


def update_categories(categories, operation):
    if operation.action == ModAction.ADD:
        category_add(categories, operation)

    if operation.action == ModAction.UPDATE:
        category_update(categories[(operation.code, operation.name)], operation)

    if operation.action == ModAction.INACTIVATE:
        category_inactivate(categories, operation)

    if operation.action == ModAction.MOVE:
        category_move(categories, operation)

    return categories


def category_move(categories, operation):
    category_to_move = categories[(operation.code, operation.name)]
    sub_categories_to_move = []

    for key, cat in categories.items():
        if cat.code.startswith(category_to_move.code):
            sub_categories_to_move.append(cat)

    new_parent_code = generate_new_code(operation.newParentCode, [k[0] for k in categories.keys()])
    new_parent_cat = Category(name=category_to_move.name,
                              code=new_parent_code,
                              description=category_to_move.description,
                              level=calculate_level(new_parent_code))

    category_to_move.status = CategoryStatus.INACTIVE

    categories[(new_parent_cat.code, new_parent_cat.name)] = new_parent_cat

    for sub_cat in sub_categories_to_move:
        new_sub_cat_code = sub_cat.code.replace(category_to_move.code, new_parent_cat.code)

        if new_sub_cat_code in [k[0] for k in categories.keys()]:
            parent_code = new_sub_cat_code[0:new_sub_cat_code.rfind("-")]
            new_sub_cat_code = generate_new_code(parent_code, [k[0] for k in categories.keys()])

        new_sub_cat = Category(name=sub_cat.name,
                               code=new_sub_cat_code,
                               description=sub_cat.description,
                               level=calculate_level(new_sub_cat_code))

        sub_cat.status = CategoryStatus.INACTIVE
        categories[(new_sub_cat.code, new_sub_cat.name)] = new_sub_cat


def category_inactivate(categories, operation):
    category = categories[(operation.code, operation.name)]
    category.status = CategoryStatus.INACTIVE

    for key, sub_cat in categories.items():
        if sub_cat.code.startswith(category.code):
            sub_cat.status = CategoryStatus.INACTIVE


def category_update(category, operation):
    if category.code == operation.code:
        category.name = operation.newName

        if operation.description is not None:
            category.description = operation.description


def category_add(categories, operation):
    if (operation.parentCode, operation.parentName) in categories:
        parent_category = categories[(operation.parentCode, operation.parentName)]
    else:
        for code, name in [k for k in categories.keys()]:
            if name == operation.parentName:
                parent_category = categories[(code, operation.parentName)]

    new_category_code = generate_new_code(parent_category.code, [k[0] for k in categories.keys()])

    level = calculate_level(new_category_code)

    category = Category(name=operation.name, code=new_category_code, description=operation.description, level=level)

    if parent_category is None:
        raise ValueError("Category must have an existing Parent: " + category)

    categories[(category.code, category.name)] = category


if __name__ == '__main__':
    category_data = load_categories()

    modification_data = load_modification_files()

    for mod in modification_data:
        update_categories(category_data, mod)

    save_categories(category_data)
