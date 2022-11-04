"""
    This module is to register useful functions.

"""
import sys
import time
from flask import request

from api import LOGGER, LOGGER_NAME
# from api.global_parameters import UNIQUE_URL_VISITS, CHANNEL, \
#    STATUS_MANAGEMENT, pika, set_channel_pika
import api.global_parameters as api_parameters


def count_unique_visits(base_url: str = '',
                        user: str = '') -> None:
    """
    Count the unique visit on the website

    :param base_url: url to count the visits
    :param user: id of the user

    :return: Nothing
    """

    if base_url in api_parameters.UNIQUE_URL_VISITS:
        if user not in api_parameters.UNIQUE_URL_VISITS[base_url]:
            api_parameters.UNIQUE_URL_VISITS[base_url].append(user)
    else:
        api_parameters.UNIQUE_URL_VISITS[base_url] = [user]

    return


def record_visit() -> (str, str, str):
    """
    Function that register who is visit the path

    :return: tuple with basic information
    """

    meth = request.method
    user = request.remote_addr
    base_url = request.base_url

    api_parameters.CHANNEL.basic_publish(
        exchange='',
        routing_key='api_amqp',
        body='{}-{}-{}'.format(user, base_url, meth))

    return base_url, meth, user


def record_message(message: str) -> bool:
    """
    Function that register who is visit the path

    :return: tuple with basic information
    """

    state = True
    try:
        api_parameters.CHANNEL.basic_publish(
            exchange='',
            routing_key='api_amqp',
            body=message)
    except Exception as e:
        print(e)
        state = False

    return state


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


def process_management(conn = None) -> None:
    # channel_pika: pika.BlockingConnection.channel
    count_time = 0

    # set_channel_pika(channel_pika)

    record_message('Starting process management')

    while api_parameters.STATUS_MANAGEMENT:
        record_message('Doing stuff on process management. Time {}'.format(count_time))
        time.sleep(5)
        count_time += 1
        if count_time > 5:
            break

    record_message('Finishing process management')
    api_parameters.CHANNEL.stop_consuming()

    [api_parameters.PROCESS_RUNNING[_k].terminate()
     for _k in api_parameters.PROCESS_RUNNING
     if 'process' in _k]

    api_parameters.PROCESS_RUNNING = {}

    return None


def process_channel(
        # channel_pika: pika.BlockingConnection.channel,
        num_channel: int) -> None:
    count_time = 0

    # set_channel_pika(channel_pika)

    record_message('Starting process channel {}'.format(num_channel))

    while True:
        record_message('Doing stuff on process channel {}. '
                       'Time {}'.format(num_channel, count_time))
        time.sleep(1)
        count_time += 1
        if count_time > 125:
            break

    record_message('Finishing process channel {}'.format(num_channel))

    api_parameters.CHANNEL.stop_consuming()

