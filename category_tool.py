import yaml


def load_categories():
    with open('src/categories-coded.yml', 'r', encoding='utf-8') as categories_file:
        categories_dict = yaml.load(categories_file)

    for k in categories_dict['categories']:
        for j, v in k.items():
            print("{} >> {}".format(j, v))

    return categories_dict


def save_categories(categories):
    with open('src/categories-coded.yml', 'w', encoding='utf-8') as categories_file:
        yaml.dump(categories, categories_file)


def load_modfile():
    with open('diff-example.yml', 'r', encoding='utf-8') as modfile:
        mod_dict = yaml.load(modfile)

    for k in mod_dict['modifications']:
        for j, v in k.items():
            print("{} >> {}".format(j, v))

    return mod_dict


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
    for mod in modifications['modifications']:
        update_categories(categories, mod)

    save_categories(categories)
