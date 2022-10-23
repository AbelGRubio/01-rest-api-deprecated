import threading

from nexiona import LOGGER
from nexiona.functions import count_unique_visits
from nexiona.global_parameters import CHANNEL


def run_amqp():
    """
    Start a AMQP queue

    :return: Nothing
    """

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
                CHANNEL.stop_consuming()
            else:
                user, base_url, meth = body.decode('utf8').split('-')

                LOGGER.info(f'VISITS: The user {user} has visited the url {base_url} '
                            f'under the method {meth}')

                count_unique_visits(base_url=base_url, user=user)

        except Exception as e:
            LOGGER.error('Error doing things. {}'.format(e))

    CHANNEL.basic_consume(queue='nexiona_amqp',
                          on_message_callback=callback,
                          auto_ack=True)

    LOGGER.info(' [*] Waiting for messages.')
    CHANNEL.start_consuming()


def declare_thread_ampq() -> None:
    """
    Just declare the amqp thread.

    :return: Nothing
    """

    th = threading.Thread(target=run_amqp,
                          name='Thread_AMPQ')
    th.start()


if __name__ == '__main__':
    declare_thread_ampq()

    f = 1
