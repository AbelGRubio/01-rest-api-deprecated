"""
    This module is to define the global parameters

"""

from flask import Flask
import pika


APP = Flask(__name__)
UNIQUE_URL_VISITS = {}

CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost',))
CHANNEL = CONNECTION.channel(channel_number=0)
CHANNEL.queue_declare(queue='api_amqp')

PROCESS_RUNNING = {}
STATUS_MANAGEMENT = True


def set_channel_pika(channel_pika: pika.BlockingConnection.channel):
    global CHANNEL

    if CHANNEL:
        CHANNEL.close()

    CHANNEL = channel_pika

