"""
    This is the main module to execute the REST API using AMPQ
    something
    eee
e e e

"""
from rest_api_agr.routes import (
    main_route, stop_endpoint, start_endpoint,
    result_endpoint, restart_endpoint)
from rest_api_agr.AMQP import declare_thread_ampq
import sys
from rest_api_agr.functions import LOGGER
from rest_api_agr.global_parameters import APP
import gunicorn


def app():
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = 'localhost'

    LOGGER.info('Setting the REST API to http://{}:5000'.format(host))

    declare_thread_ampq()

    APP.run(host=host)


if __name__ == '__main__':
    app()
