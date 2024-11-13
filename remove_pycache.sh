#!/bin/bash
DIR=$(dirname "$(realpath "$0")")

find $DIR -type d -name "__pycache__" -exec rm -rf {} +
