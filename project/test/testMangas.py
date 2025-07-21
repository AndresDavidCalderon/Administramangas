import unittest
from fastapi.testclient import TestClient
from ..src.main import app

client = TestClient(app)

class TestMangas(unittest.TestCase):

    def test_anadir_manga(self):
        response = client.post("/mangas/add", json={"title": "The seven deadly sins", "author": "Nakaba Suzuki"})
        self.assertEqual(response.status_code, 201)
        
        newMangas = client.get("/mangas/list")
        self.assertEqual(newMangas.status_code, 200)
        mangalist = newMangas.json()
        self.assertIn({"title": "The seven deadly sins", "author": "Nakaba Suzuki"}, mangalist)

    def test_eliminar_manga(self):

        response = client.delete("/mangas/delete/Attack+on+titan")
        self.assertEqual(response.status_code, 200)
        
        newMangas = client.get("/mangas/list")
        self.assertEqual(newMangas.status_code, 200)
        mangalist = newMangas.json()
        self.assertNotIn({"title": "Attack on titan", "author": "Hajime Isayama"}, mangalist)

    def test_lista_de_mangas(self):
        client.post("/mangas/add", json={"title": "The seven deadly sins", "author": "Nakaba Suzuki"})
        client.post("/mangas/add", json={"title":"Say the right thing", "author": "Kouji Seo"})
        response = client.get("/mangas/list")
        self.assertEqual(response.status_code, 200)
        mangalist = response.json()
        self.assertIn({"title": "The seven deadly sins", "author": "Nakaba Suzuki"}, mangalist)
        self.assertIn({"title": "Say the right thing", "author": "Kouji Seo"}, mangalist)