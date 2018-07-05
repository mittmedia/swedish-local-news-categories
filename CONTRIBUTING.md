# How to contribute

Input from other local news companies is vital for the category tree to stay relevant and up to date.
Follow the guidelines below before you open a pull request.

When applying a change to the tree it should be done to the file `categories-coded.yml`. If you add a new category, you need to generate a new code for that category and compute the full category code by prepending the parent code. The same is true if you suggest a move of the categories, you would have to generate new codes for the affected categories. Also, you need to to run the script that generates new derived files from the master by running the script `generate-from-yml.py` before issuing a pull request.

You also need to increment the version number in the master file when changing the tree. Use the section `Tree version` in the project readme to figure out what should be incremented in the tree version. For example, adding or removing a category would result in incrementing the second most significant number and setting the least significant to 0.

## Getting Started

* Make sure you have a [GitHub account](https://github.com/signup/free).
* Open an issue on the repo to discuss the changes.
  * Clearly describe the issue you have, don't forget to mention what problem you want to solve.
  * Make sure you reference the version of the tree you have an issue with, it will make it easier to identify outdated issues.
* Fork the repository on GitHub.
* When applying the change, do it to the file `categories-coded.yml` and run the script that generates the other file formats locally.

## Making Changes

* Create a topic branch from where you want to base your work.
  * This is usually the master branch.
  * Only target release branches if you are certain your fix must be on that
    branch.
  * To quickly create a topic branch based on master, run `git checkout -b
    fix/master/my_contribution master`. Please avoid working directly on the
    `master` branch.
* Make commits of logical and atomic units.
  * Make sure the YAML-file is still in valid YAML-format after the change. [Here's an example of an online YAML-validator](http://www.yamllint.com)
  * Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure your commit messages are in the proper format. If the commit
  addresses an issue include the issue number within parenthesis at the start of the branch name.

Here is an example of a valid pull request format

  ```
      (25) Change the description of category X
  ```
* Run the generation script without error and try to make sure that the derived files have been generated correctly.

## Making Trivial Changes

For changes in names or descriptions of categories it's not always needed to open an issue on GitHub, eg. typos.

If an issue discussing the change already exists, you can help by using the issue number in the pull request as described above.

## Submitting Changes

* Push your changes to a topic branch in your fork of the repository.
* Submit a pull request to the repository in the Mittmedia organization.
* Update your GitHub issue to mention that you've submitted a pull request.
  * Include a link to the pull request in the issue thread.
* The development team at Mittmedia will then review the pull request and offer feedback as comments on the pull request. The feedback might be to close the pull request if we feel it does not align with the project scope.
* After feedback has been given we expect responses within two weeks. After two
  weeks we may close the pull request if it isn't showing any activity.

## Revert Policy

By validating the master file, running the scripts in advance and making sure that the version number match the appropriate change, you can be more condifent that your submission will be a part of the new category tree iteration. If however the category suggestion is out of line with the project scope or does not conform to the specification laid out in the documentation, but is still accepted, Mittmedia might choose to revert the commit at a later time.

The original contributor will be notified of the revert in the GitHub issue
associated with the change.
