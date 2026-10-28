from app import  app



def test_app_online_status():
    client = app.test_client()
    response = client.get("/online")
    assert response.status_code == 200


def test_json_status():
    client = app.test_client()
    response = client.get("/online")
    data = response.get_json()
    assert data["status"] == "online"
    assert data["application"] == "alive"


def test_not_found():
    client = app.test_client()
    response = client.get("/NOT_FOUND")
    assert response.status_code == 404
   

