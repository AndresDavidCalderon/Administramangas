from fastapi.testclient import TestClient
from ..main import app
import unittest
import datetime

client = TestClient(app)

class TestPrestamos(unittest.TestCase):

    def test_renovar_prestamo(self):
        responsePrestar = client.post("/prestamos/add", json={
            "titulo_manga": "Attack on titan",
            "email_usuario": "user@example.com",
            "fecha": datetime.datetime.now().date().isoformat()
        })
        self.assertEqual(responsePrestar.status_code, 201)

        responseRenovar = client.post("/prestamos/renovar", json={
            "titulo_manga": "Attack on titan", 
            "email_usuario": "user@example.com",
            "fecha": (datetime.datetime.now().date() + datetime.timedelta(days=15)).isoformat()
        })
        self.assertEqual(responseRenovar.status_code, 200)

        prestamos = client.get("/prestamos/list")
        self.assertEqual(prestamos.status_code, 200)
        prestamos_list = prestamos.json()
        self.assertIn({
            "titulo_manga": "Attack on titan",
            "email_usuario": "user@example.com",
            "vence": (datetime.datetime.now().date() + datetime.timedelta(days=15)).isoformat()
        }, prestamos_list)