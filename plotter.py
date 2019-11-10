import json
import os
from logging import config, getLogger


config.fileConfig('log.ini', disable_existing_loggers=False)
logger = getLogger()

_TO_PESO = 28500.0
_TO_UF = 1.0 / _TO_PESO

_DATA_ROOT = 'data'
_DATA_CURR_PESOS = 1
_DATA_CURR_UF = 2

if __name__ == '__main__':
    logger.info(' >> START!')

    directory = os.fsencode('./data/')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        logger.info('opening "%s"', filename)

        price = {
            'mean': 0,
            'max': -1,
            'min': 1E10,
        }
        with open('./data/' + filename, 'r') as json_file:
            data = json.load(json_file)
            for d in data[_DATA_ROOT]:
                logger.info(d)
                break

    logger.info(' >> FINISHED!')
