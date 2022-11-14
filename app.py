"""
    This is the main module to execute the REST API using AMPQ

"""
import sys

import uvicorn

from api.AMQP import declare_thread_ampq
from api.routes import *
import multiprocessing
import api.global_parameters as api_global


if __name__ == '__main__':
    api_global.PID_GENERAL_PROCESS = multiprocessing.current_process()

    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        # host = 'localhost'
        host = '192.168.127.68'

    LOGGER.info('Setting the REST API to http://{}:5000'.format(host))

    declare_thread_ampq()

    uvicorn.run(
        APP, host=host, port=5000,
        reload=False, log_level="debug",
    )
