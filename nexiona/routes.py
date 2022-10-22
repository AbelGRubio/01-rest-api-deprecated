"""
    This module is used for define the REST API endpoints

"""
from flask import jsonify

from nexiona.functions import record_visit, read_logger_visits
from nexiona.global_parameters import APP
from .global_parameters import UNIQUE_URL_VISITS


@APP.route('/')
def main_route():
    """
    Example main route

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')


@APP.route('/path_1')
def path_1_route():
    """
    Example path 1 route

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')


@APP.route('/path_2')
def path_2_route():
    """
    Example path 2 route

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')


@APP.route('/path_1/sub_path_1')
def sub_path_1_1_route():
    """
    Example sub-path from path 1

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')


@APP.route('/unique_visited')
def unique_visited_route():
    """
    Get the count of unique visits that there are in each URL.
    The routes that have not been visited do not appear here

    :return: a json file
    """
    base_url, meth, _ = record_visit()

    number_of_unique_visited = {k: {'count': len(UNIQUE_URL_VISITS[k]),
                                    'user_id': UNIQUE_URL_VISITS[k]}
                                for k in UNIQUE_URL_VISITS}

    return jsonify(number_of_unique_visited)


@APP.route('/history')
def history_route():
    """
    Get the full history of the visited path

    :return: a json file
    """
    base_url, meth, _ = record_visit()

    lines = read_logger_visits()

    return jsonify(lines)


"""
    This is human readable endpoints, usually they are not included in a 
    API REST 
"""


@APP.route('/unique_visited_readable')
def unique_visited_readable_route():
    """
    Get the count of unique visits that there are in each URL.
    The routes that have not been visited do not appear here.

    :return: html file to show in the explorer
    """
    base_url, meth, _ = record_visit()

    number_of_unique_visited = ['{}:\tcount: {}\t ' \
                                'users: {}'.format(k,
                                                   len(UNIQUE_URL_VISITS[k]),
                                                   UNIQUE_URL_VISITS[k])
                                for k in UNIQUE_URL_VISITS]

    return '<br>'.join(number_of_unique_visited)


@APP.route('/history_readable')
def history_readable_route():
    """
    Get the full history of the visited path

    :return: html file to show in the explorer
    """
    base_url, meth, _ = record_visit()

    lines = read_logger_visits()

    return '<br>'.join(lines)
