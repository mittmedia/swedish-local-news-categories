# Category tree for Swedish local news

This tree is mainly developed for local newsrooms in Sweden. It's inspired by the [IPTC standard for news](http://show.newscodes.org/index.html?newscodes=medtop&lang=en-GB&startTo=Show) but a lot has been added, removed and changed to better suite Swedish institutions and interests. The supported formats are Yaml and JSON. The Yaml-file `categories-coded.yml` is the master file, any suggested changes or pull requests should reference this file.

The code of each category describes its position in the tree hierarchy and the tree's version field is for making maintenance and solving compatibility easier.

You can render an overview of the tree with our [visualization tool](https://swedish-local-news-categories.herokuapp.com/visualization/tree.html).

## Category code

A category code is a sequence that can be used to quickly lookup a category's parent categories. It's composed of three uppercase ASCII letters with its parent's category code as a prefix. This rule is applied recursively up to the root object. Each three letter group is separated by a hyphen (`-`) for ease of read and parsing. For example, a category with the code `RYF-XKI-WEG-NLU` has the category with the code `RYF-XKI-WEG` as its direct parent which in turn is a child category to the category with code `RYF-XKI`.

## Tree version

The tree file has a version field, `version`, consisting of three numbers in the form A.B.C which will increment by one depending on how big the change was compared to the previous version.

#### Differing versions of tree: A.B.x vs. A.B.y

If two trees differ in the least significant number the *name* or *description* of two categories might differ. Any functionality built around the names or descriptions can have unexpected consequences. However, the size and structure of the two trees will be equivalent and the category codes will be identical.

#### Differing versions of tree: A.x.x vs. A.y.y

If two trees differ by the second most significant number this means that in addition to changes as described above, categories have been added or removed. A code from one tree might not map to a category in the other tree, but two identical codes from both trees will map to the same category.

#### Differing versions of tree: x.x.x vs. y.y.y

In addition to changes described in the least significant and second most significant number, if the trees differ in the most significant number categories have been moved which results in structural differences between two trees. A code from one tree might map to a completely different category in another tree. You should consult the change log to figure out how to best migrate content with categories from the two different trees.

## Contributing to the repository

The guidelines for contributing to the repository is laid out in [CONTRIBUTING.md](https://github.com/mittmedia/swedish-local-news-categories/blob/master/CONTRIBUTING.md)

## Running the generate script

The script has been tested with Python 3.6. You run it with this command.

```
python generate_from_yml.py
```

It should overwrite the files in the directory `dist`.

## License

The Category tree for Swedish local news uses the MIT License.
