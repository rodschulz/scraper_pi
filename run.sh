#!/bin/bash

TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"
scrapy runspider scraper.py -o data/$TIMESTAMP.json
