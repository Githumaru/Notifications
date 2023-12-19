import requests

url = 'http://localhost:8000/mailings/'

# Данные нового клиента
data = {
    'start_datetime': '2024-01-06T21:19:52.544000Z',
    'end_datetime': '2024-01-15T21:19:52.544000Z',
    'tag': 'example_tag',
    'message_text': 'some text'
}


# Отправляем POST-запрос для создания нового клиента
response = requests.post(url, data=data)

# Печатаем ответ сервера
print(response.status_code)  # Выводим код ответа
print(response.json())      # Выводим JSON-ответ
