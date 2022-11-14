"""
    This module is to define the global parameters

"""

# from flask import Flask
from fastapi import FastAPI
import pika
import time
from api import LOGGER
import queue
import multiprocessing
import threading

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
QUEUE_PUBLISHER = queue.Queue()
TH_REGISTER = None


def set_queue_publisher(
        queue_publisher: queue):
    global QUEUE_PUBLISHER
    QUEUE_PUBLISHER = queue_publisher


def define_connection(thread_register: bool = False):
    global CONNECTION, CHANNEL, TH_REGISTER

    CONNECTION = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',
                                  port=5672,
                                  heartbeat=100))
    CHANNEL = CONNECTION.channel(channel_number=0)
    CHANNEL.queue_declare(
        queue='api_amqp',
        durable=False,
        auto_delete=True)
    if thread_register:
        if TH_REGISTER is None:
            TH_REGISTER = threading.Thread(
                target=register_messages,
                name='Thread_register_messages',
                )
            TH_REGISTER.start()
        elif not TH_REGISTER.is_alive():
            th = threading.Thread(
                target=register_messages,
                name='Thread_register_messages',
                )
            th.start()
        else:
            add_message_queue('Already initiated thread logger')


def define_queue_process(
        channel: pika.BlockingConnection.channel,
        process_name: str):
    channel.queue_declare(queue=process_name,
                          durable=False,
                          auto_delete=True)


def add_message_queue(message: str):
    global QUEUE_PUBLISHER
    QUEUE_PUBLISHER.put(message)


def record_message(
        message: str,
        channel: pika.BlockingConnection.channel = None,
        try_number: int = 0
    ) -> bool:
    """
    Function that register who is visit the path

    :return: tuple with basic information
    """
    if channel is None:
        global CHANNEL
        channel = CHANNEL

    state = True
    if try_number > 2:
        return False

    try:
        channel.basic_publish(
            exchange='',
            routing_key='api_amqp',
            body=message)
    except Exception as e:
        LOGGER.warning(f'Reopening connection in 2 seconds. Warning issue: {e}')
        time.sleep(2)
        define_connection()
        record_message(message)

    return state


def register_messages():
    """
    TODO: This function close when the process died

    :return:
    """
    global QUEUE_PUBLISHER

    while STATUS_CHANNEL:
        message = QUEUE_PUBLISHER.get()
        record_message(message)

