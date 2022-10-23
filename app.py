"""
    This is the main module to execute the REST API

"""

from nexiona.routes import *
from nexiona.AMQP import declare_thread_ampq

if __name__ == '__main__':
    declare_thread_ampq()

    APP.run(host='localhost',
            port=5000)
