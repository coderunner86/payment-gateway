from fastapi.testclient import TestClient

from main import app


class TestAPI:
    def setup_class(self):
        self.client = TestClient(app)

    def test_get_example(self):
        response = self.client.get("/api/examples/1")
        assert response.status_code == 200
        assert response.json() == {
            "statusCode": 200,
            "message": "Get resource successful",
            "error": None,
            "data": {
                "name": "string",
                "lastName": "string",
                "id": 1,
                "createdAt": "2023-08-01T17:23:13.219000+00:00",
                "updatedAt": "2023-08-01T17:23:13.219000+00:00",
            },
        }
