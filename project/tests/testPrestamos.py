from fastapi.testclient import TestClient
from ..main import app
import unittest
import datetime

client = TestClient(app)

class TestPrestamos(unittest.TestCase):

    def test_renovar_prestamo(self):
        client.delete("/mangas/reset")
        responsePrestar = client.post("/prestamos/add", json={
            "titulo_manga": "Attack on titan",
            "email_usuario": "ancalderonj@unal.edu.co",
            "fecha": datetime.datetime.now().date().isoformat()
        })
        self.assertEqual(responsePrestar.status_code, 200, msg="Error prestando manga, respuesta: " + responsePrestar.json()["message"])

        responseRenovar = client.patch("/prestamos/renovar?email_usuario=ancalderonj@unal.edu.co&titulo_manga=Attack%20on%20titan&fecha=" + (datetime.datetime.now().date() + datetime.timedelta(days=15)).isoformat())
        self.assertEqual(responseRenovar.status_code, 200,msg="Error renovando prestamo, respuesta: " + responseRenovar.json()["message"])