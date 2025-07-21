from fastapi.testclient import TestClient
from ..src.main import app
import unittest
import datetime

client = TestClient(app)

class TestPrestamos(unittest.TestCase):

    def test_renovar_prestamo(self):
        responsePrestar = client.post("/prestamos/add", json={"manga": "Attack on titan", "doc_usuario": 1, "manga_garantia": {
            "title": "The promised neverland", "author": "Kaiu Shirai"
        }})
        self.assertEqual(responsePrestar.status_code, 201)

        responseRenovar = client.post("/prestamos/renovar", json={"manga": "Attack on titan", "doc_usuario": 1})
        self.assertEqual(responseRenovar.status_code, 200)

        prestamos = client.get("/prestamos/list")
        self.assertEqual(prestamos.status_code, 200)
        prestamos_list = prestamos.json()
        self.assertIn({"manga": "Attack on titan", "doc_usuario": 1,"vence": (datetime.datetime.now().date() + datetime.timedelta(days=16)).isoformat()}, prestamos_list)