import threading
import time
from multiprocessing import Process

from fastapi import Request
from fastapi.responses import HTMLResponse

import api.global_parameters as api_global
from api.functions import record_visit, \
    process_channel, process_management, LOGGER
from api.global_parameters import APP, PROCESS_RUNNING


@APP.post('/close_api', response_class=HTMLResponse)
def close_programme(request: Request):
    """
    Finish the programme

    Arguments:
    - **request**:  request information by default

    """
    base_url, meth, _ = record_visit(request)

    th = threading.Thread(target=close_programme_action,
                          name='thread_to_close',
                          args=(api_global.PID_GENERAL_PROCESS.pid,),
                          )
    th.start()

    return HTMLResponse(
        content=f'Closing the programme in 5 seconds',
        status_code=200)


def close_programme_action(pid):
    cont = 0
    total_seconds = 5
    while cont < total_seconds:
        LOGGER.info(f'Closing the programme in {total_seconds - cont}')
        time.sleep(1)
        cont += 1

    os.system(f'taskkill /F /PID {pid}')


@APP.post('/start_{channel_num}', response_class=HTMLResponse)
def start_endpoint(
        channel_num: str,
        request: Request):
    """
    Function to start processing a channel

    Arguments:
    - **channel_num**: channel number
    - **request**:  request information by default

    """

    base_url, meth, _ = record_visit(request)

    name_process = 'process-{}'.format(channel_num)

    if name_process not in PROCESS_RUNNING:
        p = Process(name=name_process, target=process_channel,
                    args=(int(channel_num),))
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
