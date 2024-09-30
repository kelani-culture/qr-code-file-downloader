from typing import Dict

import pytest
from faker import Faker


@pytest.fixture
def fake_user() -> Dict[str, str]:
    fake = Faker()
    return {"email": fake.email(), "password": fake.password()}


def test_user_signup_successfully(client, fake_user):
    """
    Test user registration was successful
    """

    # Use `json` instead of `data` to send a JSON payload
    resp = client.post(
        "/user/signup", json=fake_user, headers={"Content-Type": "application/json"}
    )

    # Assert status code
    assert resp.status_code == 201

    # Assert the response body matches the expected output
    assert resp.json() == {
        "message": "User registration successful",
        "status_code": 201,
    }


# def test_user_signup_unsuccessful(client, fake_user):
#     """
#     test user registration was unsuccessful
#     """
#     data = {"email": fake_user["email"], "password": fake_user["password"]}
#     resp = client.post(
#         "/user/signup", json=data, headers={"Content-Type": "application/json"}
#     )
#     assert resp.status_code == 400

#     # assert resp body
#     assert resp.json() == {
#         "message": "User email already exists please login",
#         "status_code": 400,
#     }
