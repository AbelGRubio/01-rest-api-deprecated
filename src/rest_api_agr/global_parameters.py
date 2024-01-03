"""
    This module is to define the global parameters



eeempty
"""

from flask import Flask
import pika


APP = Flask(__name__)
UNIQUE_URL_VISITS = {}

CONNECTION, CHANNEL = None, None

# CONNECTION = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost',
#                               port=5672,
#                               heartbeat=10))
# CHANNEL = CONNECTION.channel()
# CHANNEL.queue_declare(queue='api_amqp', durable=False)

PROCESS_RUNNING = {}
STATUS_MANAGEMENT = True
STATUS_CHANNEL = True

# def set_channel_pika(channel_pika: pika.BlockingConnection.channel):
#     global CHANNEL
#
#     if CHANNEL:
#         CHANNEL.close()
#
#     CHANNEL = channel_pika


def define_connection():
    global CONNECTION, CHANNEL

    CONNECTION = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',
                                  port=5672,
                                  heartbeat=10))
    CHANNEL = CONNECTION.channel(channel_number=0)
    CHANNEL.queue_declare(queue='api_amqp', durable=False)
