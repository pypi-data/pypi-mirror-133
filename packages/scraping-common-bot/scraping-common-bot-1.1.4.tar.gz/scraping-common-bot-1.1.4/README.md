# Scraping Common Bot

### Lint
```sh
pylint -f colorized src/scraping_common_bot
```

### Build

- Before building you need to define a git tag, that git tag will be used as version:

```sh
git tag 1.0.0
tox -e build
```

- After that you can install also on local the same version:

```sh
pip install -e .
pipenv install -e .
```

### Publish

- To publish the package run this:

```sh
tox -e publish
tox -e publish -- --repository pypi
tox -av
```

More info [here](https://github.com/pyscaffold/pyscaffold)
