import requests

def send_message_to_api(client_id, message_text):
    api_url = 'https://probe.fbrq.cloud/v1/send'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzIwMTI0ODUsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9rMHRpa2JlZ2Vtb3RpayJ9.dRvWpliQ_oPoxWq3okyv1osZF_2yMJN6ON4oWTWSYYs'
    }
    data = {
        'client_id': client_id,
        'message_text': message_text
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 200:
            return True, "Сообщение успешно отправлено"
        else:
            return False, "Ошибка при отправке сообщения"

    except requests.RequestException as e:
        return False, f"Ошибка при отправке запроса: {str(e)}"

