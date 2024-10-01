from service.utils import hash_password, verify_hash_password

hashed_password = "$2b$12$4YUIjWNhY3bKICJsP0n0PePP5.x8aCw7Tvj9qlupjW0FrMoRLa1Iq"
password = "mkqnkfn12eAAfq"
def test_hashed_password(mocker):
    
    mock_hatch = mocker.patch("service.utils.pwd_context.hash", return_value=hashed_password)


    hashed = hash_password(password)

    mock_hatch.assert_called_once_with(password)    
    assert hashed == hashed_password


def test_user_password_correct(mocker):
    mock_hatch = mocker.patch("service.utils.pwd_context.verify")
    mock_hatch.return_value = True
    hashed = verify_hash_password(password, hashed_password)

    mock_hatch.assert_called_once_with(password, hashed_password)

    assert hashed is True

    mock_hatch.reset_mock()


    wrong_pass = "wrong_pass"
    mock_hatch.return_value = False
    hashed = verify_hash_password(wrong_pass, hashed_password)
    mock_hatch.assert_called_once_with(wrong_pass, hashed_password)
    assert hashed is False


# test user login function
def test_user_login(db_session):
    ...

