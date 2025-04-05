<img src="/images/icon.png" alt="Waste Collection Schedule logo" title="NEO Watcher" align="right" height="60" />

# Contributing To NEO Watcher

![python badge](https://img.shields.io/badge/Made%20with-Python-orange)
![github contributors](https://img.shields.io/github/contributors/danq8/hacs_neo_watcher?color=orange)
![last commit](https://img.shields.io/github/last-commit/danq8/hacs_neo_watcher?color=orange)

There are several ways of contributing to this project, including:

- Adding new sensors
- Updating or improving the documentation
- Helping answer/fix any issues raised

### Fork And Clone The Repository, And Checkout A New Branch

In GitHub, navigate to the repository [homepage](https://github.com/danq8/hacs_neo_watcher). Click the `fork` button at the top-right side of the page to fork the repository.

Navigate to your fork's homepage, click the `code` button and copy the url.

On your local machine, open a terminal and navigate to the location where you want the cloned directory. Type `git clone` and paste in the url copied earlier. It should look something like this, but with your username replacing `YOUR-GITHUB-USERNAME`:

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/hacs_neo_watcher
```

Before making any changes, create a new branch to work on.

```bash
git branch <new_branch_name>
```

For example, if you were adding a new sensor called fastest object, you could do

```bash
git branch adding fastest object
```

For more info on forking/cloning a repository, see GitHub's [fork-a-repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo) document.### Fork And Clone The Repository, And Checkout A New Branch

### Sync Branch and Create A Pull Request

Having completed your changes, sync your local branch to your GitHub repo, and then create a pull request. When creating a pull request, please provide a meaningful description of what the pull request covers. Confirm the .py, .md, README and info.md files have all been updated, and the output of the test_sources.py script demonstrating functionality. Once submitted a number of automated tests are run against the updated files to confirm they can be merged into the master branch. Note: Pull requests from first time contributors also undergo a manual code review before a merge confirmation in indicated.

Once a pull request has been merged into the master branch, you'll receive a confirmation message. At that point you can delete your branch if you wish.

## Update Or Improve The Documentation

Non-code contributions are welcome. If you find typos, spelling mistakes, or think there are other ways to improve the documentation please submit a pull request with updated text. Screenshots are also welcome.

## Help Answer/Fix Issues Raised

![GitHub issues](https://img.shields.io/github/issues-raw/mampfes/hacs_waste_collection_schedule?color=orange)

Open-source projects are always a work in progress, and [issues](https://github.com/danq8/hacs_neo_watcher/issues) arise from time-to-time. If you come across a new issue, please raise it. If you have a solution to an open issue, please raise a pull request with your solution.
