import time
from MqConfigs import *
from MailSender import GmailFileSender
import json
import os


def callback(ch, method, properties, body):
    mailSender = GmailFileSender()
    email = json.loads(body.decode())
    print(email)
    try:
        print (email['attachment'][1:])
        mailSender.send_email(email['receipts_mail'], email['subject'], email['body'], email['attachment'][1:])
    except Exception as e:
        #todo logar a exceção em algum lugar
        print(e)
    finally:
        time.sleep(5)


# Create an instance of RabbitMQHandler for consuming

def main_thread_conection():
    consumer = RabbitMQHandler(queue_name='emails_a_enviar', host='localhost', port=5672)
    consumer.connect()
    consumer.consume_messages(callback)


if __name__ == '__main__':
    # print (os.listdir('uploads'))
    main_thread_conection()