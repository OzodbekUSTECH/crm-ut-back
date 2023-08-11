import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

# Здесь будет храниться полученный токен
access_token = ""

def test_login_endpoint():
    global access_token  # Делаем access_token доступным для изменения в этой функции
    # Define test user credentials
    test_user_data = {
        "username": "ozod.naimov@mail.ru",
        "password": "stringst!2S"
    }

    # Make a POST request to the login endpoint
    response = client.post("/v1/users/login", data=test_user_data)

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Получаем токен из JSON-ответа
    access_token = response.json()["access_token"]

    # Assert that the response contains the expected keys
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_get_own_user_data():
    global access_token  # Используем сохраненный access_token

    # Создаем заголовок с авторизационными данными (используя полученный токен)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Отправляем GET-запрос на эндпоинт
    response = client.get("/v1/users/me", headers=headers)

    # Утверждаем, что статус-код ответа равен 200 OK
    assert response.status_code == 200

    # Утверждаем, что поля совпадают с ожидаемыми
    response_json = response.json()
    assert "id" in response_json
    assert "email" in response_json
    assert "company_name" in response_json
    assert "phone_number" in response_json
    assert "is_traveler_expert" in response_json
    assert "is_traveler" in response_json


# def test_forgot_password():
#     # Создаем мок-объект для EmailSender


#     # Отправляем POST-запрос на эндпоинт
#     response = client.post("/v1/users/forgot/password", params={"email": "ozod.naimov@mail.ru"})

#     # Утверждаем, что статус-код ответа равен 200 OK
#     assert response.status_code == 200

#      # Утверждаем, что ответ содержит ожидаемое сообщение
#     assert response.json() == {"message": "Reset Password sent successfully"}


# def test_reset_password():

#     param = {
#         "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvem9kLm5haW1vdkBtYWlsLnJ1IiwiZXhwIjoxNjkxNTc1NjgxfQ.GLxCQd76C40cl2ZkaY5BPPvupGW4SyimTbEqDRtkrFo"
#     }

#     json = {
#         "password1": "ozodbeknaimov!2S",
#         "password2": "ozodbeknaimov!2S"
#     }

#     response = client.post("/v1/users/reset/password", params=param, json=json)

#     assert response.status_code == 200

#     assert response.json() == {"message": "password has been changed successfully"}


# def test_create_user():

#     user_data = {
#         "email": "user@example.com",
#         "password": "password!2S",
#         "company": "company",
#         "is_traveler_expert": True
#     }

#     response = client.post('/v1/users', json=user_data)

#     assert response.status_code == 200

#     response_json = response.json()
#     assert "id" in response_json
#     assert "email" in response_json
#     assert "company_name" in response_json
#     assert "phone_number" in response_json
#     assert "is_traveler_expert" in response_json
#     assert "is_traveler" in response_json


def test_update_user_data():

    user_data = {
        "email": "wtf@mail.ru",
        "company": "ozodomcompany",
        "is_traveler_expert": True
    }


    response = client.put('/v1/users/15', json=user_data)

    assert response.status_code == 200

    response_json = response.json()
    assert "id" in response_json
    assert "email" in response_json
    assert "company_name" in response_json
    assert "phone_number" in response_json
    assert "is_traveler_expert" in response_json
    assert "is_traveler" in response_json