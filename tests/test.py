import requests
from pytest_voluptuous import S

from schemas.User import user

mainUrl = 'https://reqres.in/api/'
testUser = {
    "id": 999,
    "email": "test@user.ru",
    "password": "123"
}


def test_status_code():
    response = requests.get(url=mainUrl + 'users?page=1')

    assert response.status_code == 200


def test_schema():
    response = requests.get(url=mainUrl + 'users/2')
    assert S(user) == response.json()['data']


def test_login_successful():
    response = requests.post(url=mainUrl + 'login', json={
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    })

    assert response.status_code == 200
    assert len(response.json().get('token')) >= 1


def test_delete_unsuccessful():
    response = requests.post(url=mainUrl + 'login', json={
        "email": "eve.holt@reqres.in"
    })

    assert response.status_code == 400
    assert response.json().get('error') >= 'Missing password'


def test_create_successful():
    response = requests.post(url=mainUrl + 'users', json=testUser)

    assert response.status_code == 201
    assert response.reason == 'Created'
