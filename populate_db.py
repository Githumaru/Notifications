import os
import django

# Указываем путь к вашему файлу с настройками Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service.settings')

# Загружаем настройки Django
django.setup()
import random
import string
from datetime import timedelta
from django.utils import timezone
from SDG.models import Mailing, Message, Client




def generate_random_phone_number():
    return '7' + ''.join(random.choices(string.digits, k=10))

def generate_random_message():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=50))

def generate_random_datetime():
    return timezone.now() + timedelta(days=random.randint(1, 30))


def populate_mailings_and_messages_and_clients(num_records=10):
    clients = []
    for _ in range(num_records):
        phone_number = generate_random_phone_number()
        mobile_operator_code = random.choice(['XYZ', 'ABC', 'DEF'])  # Примеры кодов операторов
        tag = random.choice(['QWE', 'ASD', 'ZXC', 'QAZ'])  # Пример произвольной метки
        timezone_info = random.choice(['GMT+3', 'GMT+5', 'GMT+7'])  # Пример часового пояса
        client = Client.objects.create(
            phone_number=phone_number,
            operator_code=mobile_operator_code,
            tag=tag,
            timezone=timezone_info
        )
        clients.append(client)

    for _ in range(num_records):
        start_datetime = generate_random_datetime()
        end_datetime = start_datetime + timedelta(days=random.randint(1, 10))
        message_text = generate_random_message()
        tag = random.choice(['QWE', 'ASD', 'ZXC', 'QAZ'])
        mailing = Mailing.objects.create(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            message_text=message_text,
            tag=tag,
        )
    # Создание сообщений связанных с рассылкой
    #clients = Client.objects.all()  # Получаем всех клиентов
    for client in clients:
        sending_status = random.choice(["Sent", "Pending"])  # Пример статуса отправки
        #client.save()
        Message.objects.create(
            sending_status=sending_status,
            mailing=mailing,
            client=client,
        )

if __name__ == "__main__":
    populate_mailings_and_messages_and_clients()