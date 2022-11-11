"""
    This module is to register useful functions.

"""
import time
from fastapi import Request

from api import LOGGER, LOGGER_NAME
import api.global_parameters as api_global
import threading
import pika


def count_unique_visits(base_url: str = '',
                        user: str = '') -> None:
    """
    Count the unique visit on the website

    :param base_url: url to count the visits
    :param user: id of the user

    :return: Nothing
    """

    if base_url in api_global.UNIQUE_URL_VISITS:
        if user not in api_global.UNIQUE_URL_VISITS[base_url]:
            api_global.UNIQUE_URL_VISITS[base_url].append(user)
    else:
        api_global.UNIQUE_URL_VISITS[base_url] = [user]

    return


def record_visit(
        request: Request) -> (str, str, str):
    """
    Function that register who is visit the path

    :return: tuple with basic information
    """

    meth = request.method
    user = request.client.host
    base_url = request.base_url

    api_global.CHANNEL.basic_publish(
        exchange='',
        routing_key='api_amqp',
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


def process_management() -> None:
    count_time = 0

    api_global.define_connection()

    time.sleep(1)

    api_global.record_message('Starting process management')

    while api_global.STATUS_MANAGEMENT:
        api_global.record_message('Doing stuff on process management. Time {}'.format(count_time))
        time.sleep(5)
        count_time += 1

    api_global.record_message('Finishing process management')
    api_global.CHANNEL.stop_consuming()

    return None


def process_channel(
        num_channel: int = 1) -> None:
    count_time = 0

    api_global.define_connection()

    time.sleep(1)

    api_global.record_message(
        'Starting process channel {}'.format(num_channel),
    )

    define_the_threads(num_channel,
                       2,
                       api_global.CHANNEL)

    time.sleep(1)

    while api_global.STATUS_CHANNEL:
        api_global.record_message(
            'Doing stuff on process channel {}. '
            'Time {}'.format(num_channel, count_time)
        )
        time.sleep(1)
        count_time += 1

    api_global.record_message('Finishing process channel {}'.format(num_channel))

    api_global.CHANNEL.stop_consuming()


def define_thread(
        num_channel: str,
        num_thread: int,
        channel: pika.BlockingConnection.channel = None
) -> None:
    count_time = 0

    api_global.define_connection()

    time.sleep(1)

    api_global.record_message(
        'Starting thread {} channel {}'.format(num_thread, num_channel),
        channel)

    while api_global.STATUS_CHANNEL:
        api_global.record_message(
            'Doing stuff on process channel {} and thread {}. '
            'Time {}'.format(num_channel,
                             num_thread,
                             count_time),
            channel
        )
        time.sleep(0.5)
        count_time += 1

    api_global.record_message('Finishing thread {} channel {}'.format(
        num_thread,
        num_channel),
        channel
    )


def define_the_threads(
        num_channel: int,
        num_thread: int,
        channel: pika.BlockingConnection.channel = None
) -> None:

    api_global.record_message(f'Declaring threads for channel {num_channel}')

    for ni in range(1, num_thread + 1):
        th = threading.Thread(target=define_thread,
                              name='thread_{}_{}'.format(num_channel, num_thread),
                              args=(num_channel, num_thread, channel)
                              )
        th.start()

    api_global.record_message(f'Declared threads for channel {num_channel}')

# def define_connection():
#     global CONNECTION, CHANNEL
# 
#     CONNECTION = pika.BlockingConnection(
#         pika.ConnectionParameters(host='localhost',
#                                   port=5672,
#                                   heartbeat=10))
#     CHANNEL = CONNECTION.channel(channel_number=0)
#     CHANNEL.queue_declare(queue='api_amqp', durable=False)
# 
# 
# def api_global.record_message(message: str) -> bool:
#     """
#     Function that register who is visit the path
# 
#     :return: tuple with basic information
#     """
# 
#     state = True
#     try:
#         api_global.CHANNEL.basic_publish(
#             exchange='',
#             routing_key='api_amqp',
#             body=message)
#     except Exception as e:
#         print(e)
#         state = False
# 
#     return state
