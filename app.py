"""
    This is the main module to execute the REST API using AMPQ

"""
import sys
from api import LOGGER
from api.routes import *
from api.AMQP import declare_thread_ampq
import uvicorn


if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = 'localhost'

    LOGGER.info('Setting the REST API to http://{}:5000'.format(host))

    declare_thread_ampq()

    uvicorn.run(APP, host=host, port=5000,
                reload=False, log_level="debug",)
    # debug = True,
    # workers = 1, limit_concurrency = 1, limit_max_requests = 1