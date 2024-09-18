from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_webhook():
    response = client.post('/webhook')
    print(response)
    assert response.status_code == 200


def test_data():
    response = client.get('/data')
    print(response)
    assert response.status_code == 200


def test_sync_data():
    response = client.get('/sync/crm')
    print(response)
    assert response.status_code == 200

def test_get_tasks():
    response = client.get('/tasks')
    print(response)
    assert response.status_code == 200

def test_cancel_task():
    response = client.post('/tasks/cancel', json= {"task_id": ""})
    print(response)
    assert response.status_code == 200