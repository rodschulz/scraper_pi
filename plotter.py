import json
import os
from logging import config, getLogger


config.fileConfig('log.ini', disable_existing_loggers=False)
logger = getLogger()

_DATA_ROOT = 'data'

if __name__ == '__main__':
    logger.info(' >> START!')

    directory = os.fsencode('./data/')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        logger.info('opening "%s"', filename)

        with open('./data/' + filename, 'r') as json_file:
            data = json.load(json_file)
            for d in data[_DATA_ROOT]:
                logger.info(d)

    logger.info(' >> FINISHED!')
