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

PID_GENERAL_PROCESS = None


def define_connection():
    global CONNECTION, CHANNEL

    CONNECTION = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',
                                  port=5672,
                                  heartbeat=100))
    CHANNEL = CONNECTION.channel(channel_number=0)
    CHANNEL.queue_declare(queue='api_amqp', durable=False)


def define_queue_process(channel: pika.BlockingConnection.channel,
                         process_name: str):
    channel.queue_declare(queue=process_name, durable=False)


def record_message(
        message: str,
        channel: pika.BlockingConnection.channel = None
    ) -> bool:
    """
    Function that register who is visit the path

    :return: tuple with basic information
    """
    if channel is None:
        global CHANNEL
        channel = CHANNEL

    state = True
    try:
        channel.basic_publish(
            exchange='',
            routing_key='api_amqp',
            body=message)
    except Exception as e:
        print(e)
        state = False

    return state
