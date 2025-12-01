from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

API_KEY = "vectoros_dev_83hf93hf9h3f9"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_success_run_ingestion():
    payload={ "model": "ChatGPT 4.1", "input": "Who is Jeje?", "status": "success", "steps": [] }
    response = client.post(
        "/runs",
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    # 3. Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["steps"] == []
    assert "id" in data
    assert "created_at" in data

def test_missing_api_key_fails():
    payload={ "model": "ChatGPT 4.1", "input": "Who is Jeje?", "status": "success", "steps": [] }
    response=client.post(
        "/runs",
        json=payload,
       

    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"]=="Missing API key"
    
def test_wrong_api_key():
    payload={ "model": "ChatGPT 4.1", "input": "Who is Jeje?", "status": "success", "steps": [] }
    response=client.post(
        "/runs",
        json=payload,
        headers={"X-API-Key":"wrong_key"}
       

    )
    assert response.status_code == 403
    data = response.json()
    assert data["detail"]=="Invalid API key"
    

def test_error_status_requires_error_message():
    payload = {
        "model": "ChatGPT 4.1",
        "input": "Test",
        "status": "error",
        "steps": []
    }

    response = client.post(
        "/runs",
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    assert response.status_code == 422
    data = response.json()
    assert "error" in data["detail"][0]["msg"]

def test_error_field_forbidden_when_status_not_error():
    payload = {
        "model": "ChatGPT 4.1",
        "input": "Test",
        "status": "success",
        "error": "something went wrong",
        "steps": []
    }

    response = client.post(
        "/runs",
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    assert response.status_code == 422
    data = response.json()
    assert "error" in data["detail"][0]["msg"]

def test_steps_string_invalid():
    payload={
        "model":"ChatGPT 4.1",
        "input": "Test",
        "status": "success",
        "steps": "not valid"
    }
    
    response= client.post(
        "/runs",
        json=payload,
        headers={"X-API-Key":API_KEY}
    )

    assert response.status_code == 422

def test_steps_list_with_invalid_item():
    payload={
        "model":"ChatGPT 4.1",
        "input": "Test",
        "status": "success",
        "steps": ["bad",123,True]

       
    }
    response=client.post(
            "/runs",
            json=payload,
            headers={"X-API-Key":API_KEY}

        )
    
    assert response.status_code == 422


def test_nested_steps_valid():
    payload = {
        "model": "ChatGPT 4.1",
        "input": "Test",
        "status": "success",
        "steps": [
            {
                "type": "root",
                "metadata": {"info": "test"},
                "children": [
                    {"type": "child1", "metadata": {}, "children": []}
                ]
            }
        ]
    }

    response=client.post(
        "/runs",
        json=payload,
        headers={"X-API-Key":API_KEY}
    )

    assert response.status_code == 200
    data= response.json()

    assert len(data["steps"]) == 1

def test_long_input_output():
    payload={
        "model":"ChatGPT 4.1",
        "input": "A" * 50000,
        "output": "B" * 50000,
        "status": "success",
        "steps":[]
    }

    response= client.post(
        "/runs",
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    assert response.status_code == 200

def test_client_cannot_send_created_at():
    payload={
        "model": "ChatGPT 4.1",
        "input": "Test",
        "status": "success",
        "steps": [],
        "created_at": "2025-01-01T00:00:00"
    }

    response= client.post(
        "/runs",
        json=payload,
        headers={"X-API-Key":API_KEY}
    )

    assert response.status_code == 422


def test_client_custom_run_id():
    import uuid

    payload = {
        "run_id": str(uuid.uuid4()),
        "model": "ChatGPT 4.1",
        "input": "Test",
        "status": "success",
        "steps": []
    }

    response=client.post(
        "/runs",
        json=payload,
        headers={"X-API-Key":API_KEY}
    )

    assert response.status_code == 200

    assert response.json()["run_id"] == payload["run_id"]