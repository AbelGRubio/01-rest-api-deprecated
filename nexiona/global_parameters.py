"""
    This module is to define the global parameters

"""

from flask import Flask
import pika


APP = Flask(__name__)
UNIQUE_URL_VISITS = {}

CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
CHANNEL = CONNECTION.channel()
CHANNEL.queue_declare(queue='nexiona_amqp')
