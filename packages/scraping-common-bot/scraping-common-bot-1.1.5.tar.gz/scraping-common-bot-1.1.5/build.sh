#!/bin/bash

# create tag before runnign this script. e.q: git tag 1.0.0

pip uninstall scraping-common-bot;
rm -rf dist/ build/ &&
tox -e build
