#!/bin/sh -e
set -x

isort --profile black app
black app
autoflake --remove-all-unused-imports --recursive --in-place app --exclude=__init__.py
