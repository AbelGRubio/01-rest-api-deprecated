"""
    This module is to define the global parameters

"""

# from flask import Flask
from fastapi import FastAPI
import pika


description = """
Fast API to control the processing. 🚀


"""

APP = FastAPI(
    title='FastAPI Signal Processing Workflow',
    description=description,
    version='1.0.0'
)

UNIQUE_URL_VISITS = {}

CONNECTION, CHANNEL = None, None

PROCESS_RUNNING = {}
STATUS_MANAGEMENT = True
STATUS_CHANNEL = True


def define_connection():
    global CONNECTION, CHANNEL

    CONNECTION = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',
                                  port=5672,
                                  heartbeat=10))
    CHANNEL = CONNECTION.channel(channel_number=0)
    CHANNEL.queue_declare(queue='api_amqp', durable=False)
