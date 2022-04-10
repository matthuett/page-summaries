def test_ping_returns_msg_dict(client):
    expected_response = {
        "msg": {
            "environment": "test",
            "testing": True
        }
    }

    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == expected_response
