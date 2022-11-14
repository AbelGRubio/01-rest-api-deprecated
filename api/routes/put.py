from fastapi import Request
from fastapi.responses import HTMLResponse

from api.functions import record_visit, \
    LOGGER
from api.global_parameters import APP, PROCESS_RUNNING


@APP.put('/stop_{channel_num}', response_class=HTMLResponse)
def stop_endpoint(
        channel_num: str, request: Request
):
    """
    Stop a process which is running

    Arguments:
    - **channel_num**: channel number
    - **request**:  request information by default
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
                LOGGER.debug(f'Terminated manager process')
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
    - **request**:  request information by default
    """

    base_url, meth, _ = record_visit(request)

    return HTMLResponse(
        content=f'You have visited {base_url} under the method {meth}',
        status_code=200)
