# Category tree for Swedish local news

This tree is mainly developed for local newsrooms in Sweden. It's inspired by the [IPTC standard for news](http://show.newscodes.org/index.html?newscodes=medtop&lang=en-GB&startTo=Show) but a lot has been added, removed and changed to better suite Swedish institutions and interests. The supported formats are Yaml and JSON. The Yaml-file `categories-coded.yml` is the master file, any suggested changes or pull requests should reference this file.

The code of each category describes its position in the tree hierarchy and the tree's version field is for making maintenance and solving compatibility easier.

## Category code

A category code is a sequence that can be used to quickly lookup a category's parent categories. It's composed of three uppercase ASCII letters with its parent's category code as a prefix. This rule is applied recursively up to the root object. Each three letter group is separated by a hyphen (`-`) for ease of read and parsing. For example, a category with the code `RYF-XKI-WEG-NLU` has the category with the code `RYF-XKI-WEG` as its direct parent which in turn is a child category to the category with code `RYF-XKI`.

## Tree version

The tree file has a version field, `version`, consisting of three numbers in the form A.B.C which will increment by one depending on how big the change was compared to the previous version.

#### Differing versions of tree: A.B.x vs. A.B.y

If two trees differ in the least significant number the *name* or *description* of two categories might differ. Any functionality built around the names or descriptions can have unexpected consequences. However, the size and structure of the two trees will be equivalent and the category codes will be identical.

#### Differing versions of tree: A.x.x vs. A.y.y

If two trees differ by the second most significant number this means that in addition to changes as described above, categories have been added or removed. A code from one tree might not map to a category in the other tree, but two identical codes from both trees will map to the same category.

#### Differing versions of tree: x.x.x vs. y.y.y

In addition to changes described in the least significant and second most significant number, if the trees differ in the most significant number categories have been moved which results in structure differences between two trees. A code from one tree might map to a completely different category in another tree. You should consult the change log to figure out how to best migrate content with categories from the two different trees.

## Contributing to the repository

When applying a change to the tree it should be done to the file `categories-coded.yml`. If you add a new category, you need to generate a new code for that category and compute the full category code by prepending the parent code. The same is true if you suggest a move of the categories, you would have to generate new codes for the affected categories. Also, you need to to run the script that generates new derived files from the master by running the script `generate-from-yml.py` before issuing a pull request.

You also need to increment the version number in the master file when changing the tree. Use the section `Tree version` to figure out what should be incremented in the tree. For example, adding or removing a category would result in incrementing the second most significant number and setting the least significant to 0.

## Running the generate script

The script has been tested with Python 3.6. You run it with this command.

```
python generate_from_yml.py
```

It should overwrite the files in the directory `category-tree-generated`.
