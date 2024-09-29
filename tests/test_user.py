from faker import Faker
import pytest
from typing import Dict

@pytest.fixture
def fake_user() -> Dict[str, str]:
    fake = Faker()
    return {"email": fake.safe_email(), "password": fake.password()}

def test_user_signup_successfully(client, fake_user):
    """
    Test user registration was successful
    """
    data = {"email": fake_user["email"], "password": fake_user["password"]}

    # Use `json` instead of `data` to send a JSON payload
    resp = client.post("/user/signup", json=data, headers={"Content-Type": "application/json"})

    # Assert status code
    assert resp.status_code == 201
    
    # Assert the response body matches the expected output
    assert resp.json() == {"message": "User registration successful", 'status_code': 201}