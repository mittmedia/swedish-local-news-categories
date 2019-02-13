from dataclasses import dataclass
from enum import Enum

import yaml


class ModAction(Enum):
    ADD = 1
    UPDATE = 2
    MOVE = 3


@dataclass
class Category:
    code: str
    level: int
    name: str
    description: str = None
    replaces: str = None
    replacedBy: str = None


@dataclass
class ModOperation:
    action: ModAction
    code: str
    description: str = None
    name: str = None
    newParentCode: str = None
    parentName: str = None


def load_categories():
    with open('src/categories-coded.yml', 'r', encoding='utf-8') as categories_file:
        categories_dict = yaml.load(categories_file)

    categories = []

    for category in categories_dict['categories']:
        cat = Category(code=category['code'], level=category['level'], name=category['name'])

        if 'description' in category:
            cat.description = category['description']
        if 'replaces' in category:
            cat.replaces = category['replaces']
        if 'replacedBy' in category:
            cat.replacedBy = category['replacedBy']

        categories.append(cat)

    return categories


def load_modfile():
    with open('diff-example.yml', 'r', encoding='utf-8') as modfile:
        mod_dict = yaml.load(modfile)

    modifications = []

    for modification in mod_dict['modifications']:
        mod = ModOperation(action=ModAction[modification['action']], code=modification['code'])

        if 'description' in modification:
            mod.replacedBy = modification['description']
        if 'name' in modification:
            mod.name = modification['name']
        if 'newParentCode' in modification:
            mod.newParentCode = modification['newParentCode']
        if 'parentName' in modification:
            mod.parentName = modification['parentName']

        modifications.append(mod)
    return modifications

def save_categories(categories):
    with open('src/categories-coded.yml', 'w', encoding='utf-8') as categories_file:
        yaml.dump(categories, categories_file, allow_unicode=True, explicit_start=True,
                  width=4096, line_break='\n')


def update_categories(categories, mod_operation):
    if mod_operation['action'] == 'UPDATE':
        for k in categories['categories']:
            if k['code'] == mod_operation['code']:
                if 'name' in mod_operation:
                    k['name'] = mod_operation['name']
                if 'description' in mod_operation:
                    k['description'] = mod_operation['description']
    return categories


if __name__ == '__main__':
    categories = load_categories()
    modifications = load_modfile()

    print(categories)
    print(modifications)
    # for mod in modifications['modifications']:
    #     update_categories(categories, mod)

    # save_categories(categories)
