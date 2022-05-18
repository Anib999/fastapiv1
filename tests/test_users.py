from app import schemas
import pytest
from jose import jwt
# from .database import client, session
from app.config import settings

def test_root(client):
    res = client.get('/')
    print(res.json().get('message'))
    assert res.status_code == 200


def test_user_create(client):
    res = client.post(
        '/users/', json={'email': 'abc2@gmail.com', 'password': 'polo'})
    # ** means unpacking json
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'abc2@gmail.com'
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        '/logins', data={'username': test_user['email'], 'password': test_user['password']})
    login_us = schemas.Token(**res.json())
    
    payload = jwt.decode(login_us.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_us.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize('email, password, status_code', [
    ('abc@g.com', 'lolwa', 403),
    (None, 'asdf', 422),
    ('abc@g.com', None, 422)
])
def test_incorrect_user(test_user, client, email, password, status_code):
    res = client.post('/logins', data={'username': email, 'password': password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid username or password'
