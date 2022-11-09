"""
    This module is used for define the REST API endpoints

"""

# from flask import jsonify
from fastapi import Request

from api.functions import record_visit, \
    process_channel, process_management, LOGGER
from api.global_parameters import APP, PROCESS_RUNNING
from multiprocessing import Process
from fastapi.responses import HTMLResponse


# @APP.get('/', response_class=HTMLResponse)
# def main_route(request: Request):
#     """
#     Example main route
#
#     :return: a json file
#     """
#
#     base_url, meth, _ = record_visit(request)
#
#     return HTMLResponse(
#         content=f'You have visited {base_url} under the method {meth}',
#         status_code=200)
#

@APP.get('/result_{channel_num}', response_class=HTMLResponse)
def result_endpoint(channel_num: str, request: Request):
    """
    Get the result of the channel

    Arguments:
    - **channel_num**: channel number
    - **request**:  request information

    """
    base_url, meth, _ = record_visit(request)

    return f'You have visited {base_url} under the method {meth}'


@APP.post('/start_{channel_num}', response_class=HTMLResponse)
def start_endpoint(
        channel_num: str,
        request: Request):
    """
    Function to start processing a channel

    Arguments:
    - **channel_num**: channel number
    - **request**:  request information

    """

    base_url, meth, _ = record_visit(request)

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

    return HTMLResponse(
        content=f'You have visited {base_url} under the method {meth}',
        status_code=200)


@APP.put('/stop_{channel_num}', response_class=HTMLResponse)
def stop_endpoint(
        channel_num: str, request: Request
        ):
    """
    Stop a process which is running

    Arguments:
    - **channel_num**: channel number
    - **request**:  request information
    """

    base_url, meth, _ = record_visit(request)

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
                LOGGER.debug(f'Terminated process logger')
                del PROCESS_RUNNING[name_process_0]

    return HTMLResponse(
        content=f'You have visited {base_url} under the method {meth}',
        status_code=200)


@APP.put('/restart_{channel_num}', response_class=HTMLResponse)
def restart_endpoint(
        channel_num: str, request: Request):
    """
    Restart a process which is running

    Arguments:
    - **channel_num**: channel number
    - **request**:  request information
    """

    base_url, meth, _ = record_visit(request)

    return HTMLResponse(
        content=f'You have visited {base_url} under the method {meth}',
        status_code=200)
