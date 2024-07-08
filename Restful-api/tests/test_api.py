# tests/test_api.py

import pytest
from app import app, db
from models import User, TextData

@pytest.fixture(scope='module')
def test_client():
    """
    Set up a test client before running the tests.
    """
    app.config.from_object('config_test.TestConfig')
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

def test_register(test_client):
    """
    Test user registration endpoint.
    """
    response = test_client.post('/register', json={
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['msg'] == 'User registered successfully'

def test_login(test_client):
    """
    Test user login endpoint.
    """
    test_client.post('/register', json={
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password'
    })
    response = test_client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test_password'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['msg'] == 'Login successful'

def test_upload_text(test_client):
    """
    Test text data upload endpoint.
    """
    test_client.post('/register', json={
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password'
    })
    login_response = test_client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test_password'
    })
    login_data = login_response.get_json()
    user_id = User.query.filter_by(username='test_user').first().id

    response = test_client.post('/upload-text', json={
        'user_id': user_id,
        'content': 'This is a test text for sentiment analysis.'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['msg'] == 'Text data uploaded successfully'

def test_get_text_data(test_client):
    """
    Test retrieving all text data.
    """
    response = test_client.get('/text-data')
    data = response.get_json()
    assert response.status_code == 200
    assert 'text_data' in data

def test_get_user_text_data(test_client):
    """
    Test retrieving text data uploaded by a specific user.
    """
    test_client.post('/register', json={
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password'
    })
    login_response = test_client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test_password'
    })
    login_data = login_response.get_json()
    user_id = User.query.filter_by(username='test_user').first().id

    response = test_client.get(f'/text-data/{user_id}')
    data = response.get_json()
    assert response.status_code == 200
    assert 'user_text_data' in data

if __name__ == '__main__':
    pytest.main()
