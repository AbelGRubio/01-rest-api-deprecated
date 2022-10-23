"""
    This module is to register useful functions.

"""
from flask import request

from nexiona import LOGGER, LOGGER_NAME
from nexiona.global_parameters import UNIQUE_URL_VISITS, CHANNEL


def count_unique_visits(base_url: str = '',
                        user: str = '') -> None:
    """
    Count the unique visit on the website

    :param base_url: url to count the visits
    :param user: id of the user

    :return: Nothing
    """

    if base_url in UNIQUE_URL_VISITS:
        if user not in UNIQUE_URL_VISITS[base_url]:
            UNIQUE_URL_VISITS[base_url].append(user)
    else:
        UNIQUE_URL_VISITS[base_url] = [user]

    return


def record_visit() -> (str, str, str):
    """
    Function that register who is visit the path

    :return: tuple with basic information
    """

    meth = request.method
    user = request.remote_addr
    base_url = request.base_url

    CHANNEL.basic_publish(exchange='',
                          routing_key='nexiona_amqp',
                          body='{}-{}-{}'.format(user, base_url, meth))

    return base_url, meth, user


def read_logger_visits() -> list:
    """
    Read the logger to show the visit history.
    If the file not exists, the function will return

        'No history visit yet'

    :return: a list of visits
    """
    try:

        with open(r'log/{}.log'.format(LOGGER_NAME), 'r') as f:
            lines = f.readlines()

        lines = [line for line in lines if ' VISITS: ' in line]

    except FileNotFoundError:
        LOGGER.warning('No history visit yet')
        lines = ['No history visit yet']

    return lines
