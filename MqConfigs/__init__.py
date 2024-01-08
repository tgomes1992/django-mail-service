import pika

class RabbitMQHandler:
    def __init__(self, queue_name, exchange_name='', routing_key='', host='localhost', port=5672):
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.host = host
        self.port = port

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        self.channel = self.connection.channel()

        if self.exchange_name:
            self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct')

        self.channel.queue_declare(queue=self.queue_name)

        if self.exchange_name:
            self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=self.routing_key)

    def close_connection(self):
        self.connection.close()

    def publish_message(self, message, persistent=False):
        properties = pika.BasicProperties(delivery_mode=2 if persistent else 1)
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
            properties=properties
        )

    def consume_messages(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def get_messages(self, num_messages=1):
        messages = []
        for _ in range(num_messages):
            method_frame, header_frame, body = self.channel.basic_get(queue=self.queue_name, auto_ack=False)
            if method_frame:
                messages.append(body.decode())
                # self.channel.basic_ack(method_frame.delivery_tag)  # Acknowledge the message
            else:
                break
        return messages

    def get_queue_message_count(self):
        method_frame = self.channel.queue_declare(queue=self.queue_name, passive=True)
        return method_frame.method.message_count



