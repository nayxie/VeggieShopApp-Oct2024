import json
import pytest


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login(client):
    response = client.post('/login/', 
        data={'username': 'moe_m', 'password': '123456'}
    )
    assert response.status_code == 302

def test_logout(client):
    response = client.get('/logout/')
    assert response.status_code == 302

def test_register(client):
    response = client.post('/register/', 
        data={
            'first_name': 'Karl',
            'last_name': 'Marx',
            'username': 'karl_m',
            'password': 'abcdefg',
            'address': '123 High St, Auckland',
            'customer_type': 'customer'
        }
    )
    assert response.status_code == 302

def test_customer_add_to_cart(client):
    response = client.post('/customer/add_to_cart/',
        data=json.dumps({
            'product_id': 1,
            'quantity': 2,
            'name': 'Carrot',
            'price': 10.0,
            'unit': 'kg'
        }),
        content_type='application/json'
    )
    assert response.status_code == 200

def test_customer_dashboard(client, mock_session_customer):
    with client.session_transaction() as session:
        session['username'] = mock_session_customer['username']
        session['user_type'] = mock_session_customer['user_type']
    response = client.get('/customer/dashboard/')
    assert response.status_code == 200

def test_staff_dashboard(client, mock_session_staff):
    with client.session_transaction() as session:
        session['username'] = mock_session_staff['username']
        session['user_type'] = mock_session_staff['user_type']
    response = client.get('/staff/dashboard/')
    assert response.status_code == 200



@pytest.fixture
def mock_session_customer():
    return {
        'username': 'moe_m',
        'user_type': 'customer'
    }

@pytest.fixture
def mock_session_staff():
    return {
        'username': 'steve_j',
        'user_type': 'staff'
    }