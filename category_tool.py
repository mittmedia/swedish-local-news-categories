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
    code: str
    description: str = None
    name: str = None
    newName: str = None
    newParentCode: str = None
    newParentName: str = None
    parentName: str = None
    parentCode: str = None


def load_categories():
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

    categories['version'] = categories_dict['version']

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
    categories_output = {'categories': [], 'version': categories['version']}

    for key, value in categories.items():
        # If the key is a tuple it is a category # lets see if this is needed :)
        if isinstance(key, tuple):
            category = {'code': value.code, 'level': value.level, 'name': value.name, 'status': value.status.name}

            if value.description is not None:
                category['description'] = value.description

            if value.replaces is not None:
                category['replaces'] = value.replaces

            if value.replacedBy is not None:
                category['replacedBy'] = value.replacedBy

            categories_output['categories'].append(category)

    with open('src/categories-coded.yml', 'w', encoding='utf-8', newline="\n") as categories_file:
        yaml.dump(categories_output, categories_file, default_flow_style=False, allow_unicode=True,
                  explicit_start=False,
                  width=4096, line_break="\n")


def update_categories(categories, operation):
    if operation.action == ModAction.ADD:
        category_add(categories, operation)

    if operation.action == ModAction.UPDATE:
        category_update(categories[(operation.code, operation.name)], operation)

    if (operation.action == ModAction.INACTIVATE):
        category_inactivate(categories, operation)

    return categories

def category_move(categories, operation):
    print('need to move stuff')
    category = categories[(operation.code, operation.name)]
    category.status = CategoryStatus.INACTIVE

    for key, sub_cat in categories.items():
        if isinstance(key, tuple):
            if sub_cat.code.startswith(category.code):
                sub_cat.status = CategoryStatus.INACTIVE



def category_inactivate(categories, operation):
    category = categories[(operation.code, operation.name)]
    category.status = CategoryStatus.INACTIVE

    for key, sub_cat in categories.items():
        if isinstance(key, tuple):
            if sub_cat.code.startswith(category.code):
                sub_cat.status = CategoryStatus.INACTIVE


def category_update(category, operation):
    if category.code == operation.code:
        category.name = operation.newName

        if operation.description is not None:
            category.description = operation.description


def category_add(categories, operation):
    # Might need this to get it into the dict at the "right" place, also need
    parent_category = categories[(operation.parentCode, operation.parentName)]

    category = Category(name=operation.name, code=operation.code, description=operation.description)

    if parent_category is None:
        raise ValueError("Category must have an existing Parent: " + category)

    categories[(category.code, category.name)] = category


if __name__ == '__main__':
    category_data = load_categories()
    for mod in load_modfile():
        update_categories(category_data, mod)

    save_categories(category_data)
