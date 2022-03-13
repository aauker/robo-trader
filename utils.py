
import configparser
import logging
import os

logger = logging.getLogger('utils')
logger.setLevel(logging.INFO)

def get_app_logger(name):
    logging.basicConfig(format="[%(asctime)s] [%(name)s] %(levelname)s: %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

def get_config():
    ROOT_CFG_DIR = os.environ['ROOT_CFG_DIR']

    config = configparser.ConfigParser()
    config.read(f'{ROOT_CFG_DIR}/.aws/robotrader.cfg')

    logger.info(f"Loaded config: {config.sections()}")

    return config
