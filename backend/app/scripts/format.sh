#!/bin/sh -e
set -x

isort --profile black app
black app
