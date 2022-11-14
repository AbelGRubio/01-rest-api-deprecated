from fastapi import Request
from fastapi.responses import HTMLResponse, FileResponse

from api.functions import record_visit
from api.global_parameters import APP


@APP.get('/', response_class=HTMLResponse)
def root(request: Request):
    """
    Arguments:
    - **request**:  request information by default

    """

    base_url, meth, _ = record_visit(request)

    path = r'20200602165844000_00060_19900_HDASPU21021_CHA_3_WF_Measure.bmp'

    return HTMLResponse(
        content=f'You have visited {base_url} under the method {meth} '
                f'<br><br> <h1> Ask for a command '
                f'<a href="http://192.168.127.68:5000/docs"> here </a> </h1>'
        ,
        status_code=200)


@APP.get('/result_{channel_num}', response_class=HTMLResponse)
def result_endpoint(channel_num: str, request: Request):
    """
    Get the result of the channel

    Arguments:646101251
    - **channel_num**: channel number
    - **request**:  request information by default

    """
    base_url, meth, _ = record_visit(request)

    path = r'20200602165844000_00060_19900_HDASPU21021_CHA_3_WF_Measure.bmp'

    # return f'You have visited {base_url} under the method {meth}'
    return FileResponse(path=path, filename=path, media_type='bmp')
