from nexiona import LOGGER
from nexiona.functions import count_unique_visits
from nexiona.global_parameters import CHANNEL


def run_amqp():

    def callback(ch, method, properties, body):
        user, base_url, meth = body

        LOGGER.info(f'VISITS: The user {user} has visited the url {base_url} '
                    f'under the method {meth}')

        count_unique_visits(base_url=base_url, user=user)

        if body == b'stop_consuming':
            CHANNEL.stop_consuming()

    CHANNEL.basic_consume(queue='nexiona_amqp',
                          on_message_callback=callback,
                          auto_ack=True)

    LOGGER.info(' [*] Waiting for messages.')
    CHANNEL.start_consuming()


if __name__ == '__main__':
    import threading

    th = threading.Thread(target=run_amqp, )
    th.start()

    f = 1


