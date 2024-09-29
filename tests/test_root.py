


def test_root_endpoint(client):
    """
    test the root endpoint
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"info": "Welcome to pdf converter home page"}
