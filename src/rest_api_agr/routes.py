"""
    This module is used for define the REST API endpoints

"""

from flask import jsonify

from rest_api_agr.functions import record_visit, \
    process_channel, process_management, LOGGER
from rest_api_agr.global_parameters import APP, PROCESS_RUNNING
from multiprocessing import Process


@APP.route('/')
def main_route():
    """
    Example main route

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')


@APP.route('/start_<channel_num>')
def start_endpoint(channel_num: str):
    """
    Example path 1 route

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    name_process = 'process-{}'.format(channel_num)

    if name_process not in PROCESS_RUNNING:
        p = Process(name=name_process, target=process_channel,
                    args=(int(channel_num), ))
        p.daemon = True
        p.start()

        PROCESS_RUNNING[name_process] = p

        name_process_0 = 'process-0'
        if name_process_0 not in PROCESS_RUNNING:
            p = Process(name=name_process_0,
                        target=process_management,
                        )
            p.daemon = True
            p.start()
            PROCESS_RUNNING[name_process_0] = p

    return jsonify(f'You have visited {base_url} under the method {meth} '
                   f'and you started the process channel {channel_num}')


@APP.route('/stop_<channel_num>')
def stop_endpoint(channel_num: str):
    """
    Example path 2 route

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    name_process = 'process-{}'.format(channel_num)

    if channel_num == 'all':
        for pn in PROCESS_RUNNING:
            p = PROCESS_RUNNING[pn]
            p.terminate()
            LOGGER.debug(f'Terminated process {pn}')
    else:
        if name_process in PROCESS_RUNNING:
            p = PROCESS_RUNNING[name_process]
            p.terminate()
            LOGGER.debug(f'Terminated process channel {channel_num}')
            del PROCESS_RUNNING[name_process]

            if len(PROCESS_RUNNING) == 1:
                name_process_0 = 'process-0'
                p = PROCESS_RUNNING[name_process_0]
                p.terminate()
                LOGGER.debug('Terminated process logger')
                del PROCESS_RUNNING[name_process_0]

    return jsonify(f'You have visited {base_url} under the method {meth}'
                   f'and you finished the process channel {channel_num}')


@APP.route('/restart_<channel_num>')
def restart_endpoint(channel_num: str):
    """
    Example sub-path from path 1

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')


@APP.route('/result_<channel_num>')
def result_endpoint(channel_num: str):

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')

