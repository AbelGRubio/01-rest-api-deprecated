"""
    This package is to save each function and classes that
    are useful for execute the programme. The statement is:

    .. image:: ../assets/prueba_api.pdf

    To solve this problem we are going to use an API REST using
    Flask


    eee

"""
import logging
import os
import sys

from logging.handlers import TimedRotatingFileHandler


__version__ = '0.4.7'


LOGGER_NAME = "amqp_api"


def set_logger() -> logging.Logger:
    """
    Start a logger in debug level to know what happening in the programme.
    Create a logger for each day.

    :return: An initialize logger
    """

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    folder = 'log'
    if not os.path.exists(folder):
        os.mkdir(folder)
    fh = TimedRotatingFileHandler(os.path.join(folder,
                                               '.'.join([LOGGER_NAME, folder])),
                                  when='midnight')
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s '
                                  # '[%(processName)s:%(threadName)s]'
                                  # '<.%(funcName)s>'
                                  ' %(message)s',
                                  datefmt='%d/%b/%Y %H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger


LOGGER = set_logger()
