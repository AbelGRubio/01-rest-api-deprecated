"""
    This is the main module to execute the REST API using AMPQ

"""
from src.rest_api_agr.routes import *
from src.rest_api_agr.AMQP import declare_thread_ampq
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = 'localhost'

    LOGGER.info('Setting the REST API to http://{}:5000'.format(host))

    declare_thread_ampq()

    APP.run(host=host,
            port=5000)
