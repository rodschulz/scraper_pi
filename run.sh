#!/bin/bash

TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"
scrapy runspider pinmov.py -o data/$TIMESTAMP.json
