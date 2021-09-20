import logging
import os


def setup_logger(path_file_name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # define file handler and set formatter
    file_handler = logging.FileHandler(path_file_name+'.log')
    formatter = logging.Formatter(
        '%(asctime)s : %(levelname)s : %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)
    return logger
