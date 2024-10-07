from typing import Dict

import pytest
from faker import Faker

from models.users import User
from service.utils import hash_password


@pytest.fixture
def fake_user() -> Dict[str, str]:
    fake = Faker()
    f = {"email": fake.email(), "password": fake.password()}
    print(f)
    return f


# test user signup routes
def test_user_signup_successfully(client, fake_user):
    """
    Test user registration was successful
    """
    # Use `json` instead of `data` to send a JSON payload
    resp = client.post(
        "/auth/user/signup",
        json=fake_user,
        headers={"Content-Type": "application/json"},
    )

    # Assert status code
    assert resp.status_code == 201

    # Assert the response body matches the expected output
    assert resp.json() == {
        "message": "User registration successful",
        "status_code": 201,
    }


def test_user_signup_unsuccessful(client, fake_user, db_session):
    """
    test user registration was unsuccessful
    """
    user = User(**fake_user)
    db_session.add(user)
    db_session.commit()
    resp = client.post(
        "/auth/user/signup",
        json=fake_user,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400

    # assert resp body
    assert resp.json() == {
        "message": "User email already exists please login",
        "status_code": 400,
    }


# # test user login routes
# def test_user_login_successful(client, fake_user, db_session):
#     password = hash_password(fake_user["password"])
#     user = User(email=fake_user["email"], password=password)
#     db_session.add(user)
#     db_session.commit()
#     resp = client.post(
#         "/auth/user/login", json=fake_user, headers={"Content-Type": "application/json"}
#     )
#     assert resp.status_code == 200
#     assert resp.json().get("access_token") is not None
#     assert resp.json().get("refresh_token") is not None
#     assert resp.json().get("expires_in_min") is not None


# def test_user_login_unsuccessful(client, fake_user):
#     resp = client.post("/auth/user/login", json=fake_user)

#     assert resp.status_code == 400
#     assert resp.json() == {
#         "message": "Invalid email or password provided",
#         "status_code": 400,
#     }
