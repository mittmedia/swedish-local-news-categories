from dataclasses import dataclass
from enum import Enum

import yaml


class CategoryStatus(Enum):
    ACTIVE = 1
    INACTIVE = 2
    REPLACED = 3


@dataclass
class Category:
    name: str
    code: str
    level: int
    status: CategoryStatus = CategoryStatus.ACTIVE
    description: str = ''
    replaces: str = None
    replacedBy: str = None


version = None

mod_file_path = 'src/mods'


def load_category_file(file_path):
    global version
    with open(file_path, 'r', encoding='utf-8') as categories_file:
        categories_dict = yaml.safe_load(categories_file)

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
            cat.status = CategoryStatus[category['status']]

        categories[(cat.code, cat.name)] = cat

    version = categories_dict['version']

    return categories


if __name__ == '__main__':
    category_data_unsorted = load_category_file('src/categories-coded-master.yml')
    category_data = load_category_file('src/categories-coded.yml')

    for key in category_data_unsorted:
        if category_data_unsorted[key] != category_data[key]:
            raise ValueError("Category is not equal in sorted vs unsorted {}".format(key))

    for key in category_data:
        if category_data_unsorted[key] != category_data[key]:
            raise ValueError("Category is not equal in sorted vs unsorted {}".format(key))
