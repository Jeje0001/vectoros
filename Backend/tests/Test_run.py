import requests
import uuid
import json

API_KEY = "vectoros_dev_83hf93hf9h3f9"
BASE_URL = "http://127.0.0.1:8000/runs"


def send_valid_run():
    payload = {
        "model": "ChatGPT 4.1",
        "input": "Who is Jeje?",
        "status": "success",
        "steps": []
    }

    response = requests.post(
        BASE_URL,
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    print("\n=== VALID RUN RESPONSE ===")
    print("Status:", response.status_code)
    print(json.dumps(response.json(), indent=2))


def send_invalid_run():
    payload = {
        "model": "ChatGPT 4.1",
        "input": "Test invalid",
        "status": "success",
        "steps": "not-valid"    # invalid steps
    }

    response = requests.post(
        BASE_URL,
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    print("\n=== INVALID RUN RESPONSE ===")
    print("Status:", response.status_code)
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    send_valid_run()
    send_invalid_run()
