import logging
#impement using singleton

EXECUTION_TIME = "Execution time|"
INTERRUPED_FROM_KEYBOARD = "Interrupted from keyboard"


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=SingletonType):
    _logger = None

    def __init__(self, path_file_name):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)  # enable the log of all types

        # define file handler and set formatter
        file_handler = logging.FileHandler(
            mode='w', filename=path_file_name+'.log')
        formatter = logging.Formatter(
            '[%(levelname)s]\t%(message)s')
        file_handler.setFormatter(formatter)

        # add file handler to _logger
        self._logger.addHandler(file_handler)

    def get_logger(self):
        return self._logger
