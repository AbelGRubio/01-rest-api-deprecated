import threading

import api.global_parameters as api_global
from api import LOGGER
from api.functions import count_unique_visits
import functools


def run_amqp():
    """
    Start a AMQP queue

    :return: Nothing
    """
    api_global.define_connection()

    def ack_message(channel, delivery_tag):
        """Note that `channel` must be the same pika channel instance via which
        the message being ACKed was retrieved (AMQP protocol constraint).
        """
        if channel.is_open:
            channel.basic_ack(delivery_tag)
        else:
            # Channel is already closed, so we can't ACK this message;
            # log and/or do something that makes sense for your app in this case.
            pass

    def callback(ch, method, properties,
                 body: bytes = b''):
        """
        This function is called when the message has arrived


        :param ch: channel
        :param method:
        :param properties:
        :param body: message

        :return:
        """
        try:
            if body == b'stop_consuming':
                """ or ch.stop_consuming """
                api_global.CHANNEL.stop_consuming()
            else:
                try:
                    user, base_url, meth = body.decode('utf8').split('-')

                    LOGGER.debug(
                        f'VISITS: The user {user} has visited the url {base_url} '
                        f'under the method {meth}')

                    count_unique_visits(base_url=base_url, user=user)

                except ValueError:
                    LOGGER.debug(body.decode('utf8'))
        except Exception as e:
            LOGGER.error('Error doing things. {}'.format(e))

        cb = functools.partial(ack_message, ch, method.delivery_tag)
        api_global.CONNECTION.add_callback_threadsafe(cb)

        # api_global.CHANNEL.basic_ack(method.delivery_tag)

    api_global.CHANNEL.basic_consume(
        queue='api_amqp',
        on_message_callback=callback,
        auto_ack=False)

    LOGGER.info(' [*] Waiting for messages.')
    api_global.CHANNEL.basic_qos(prefetch_count=1)
    api_global.CHANNEL.start_consuming()


def declare_thread_ampq() -> None:
    """
    Just declare the amqp thread.

    :return: Nothing
    """

    th = threading.Thread(target=run_amqp,
                          name='Thread_AMPQ',
                          )
    th.start()


if __name__ == '__main__':
    declare_thread_ampq()

    f = 1
