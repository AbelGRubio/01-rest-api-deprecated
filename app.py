"""
    This is the main module to execute the REST API

"""

from nexiona.routes import *


if __name__ == '__main__':
    APP.run(host='localhost',
            port=5000)
