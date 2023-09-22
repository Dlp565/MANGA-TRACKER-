from fastapi.testclient import TestClient
from main import app
print(app)
client = TestClient(app)




def test_login():
    response = client.post("/register",
                          json={
                              "username": "test",
                              "password": "test"
                          },
                          )
    print(response)
    assert response.status_code == 200

