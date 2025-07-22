import unittest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

class TestMangas(unittest.TestCase):

    def test_anadir_manga(self):
        response = client.post("/mangas/add", json={"title": "The seven deadly sins", "author": "Nakaba Suzuki"})
        self.assertEqual(response.status_code, 201)
        
        newMangas = client.get("/mangas/list")
        self.assertEqual(newMangas.status_code, 200)
        mangalist = newMangas.json()
        self.assertIn({"title": "The seven deadly sins", "author": "Nakaba Suzuki", "usuario_ultimo_prestamo": None}, mangalist)

    def test_anadir_manga_existente(self):
        response = client.post("/mangas/add", json={"title": "Attack on titan", "author": "Hajime Isayama"})
        self.assertEqual(response.status_code, 400) # En el estado por defecto, attack on titan ya existe.
        
    def test_eliminar_manga(self):

        response = client.delete("/mangas/delete/Attack%20on%20titan")
        self.assertEqual(response.status_code, 200)
        
        newMangas = client.get("/mangas/list")
        self.assertEqual(newMangas.status_code, 200)
        mangalist = newMangas.json()
        self.assertNotIn({"title": "Attack on titan", "author": "Hajime Isayama", "usuario_ultimo_prestamo": None}, mangalist)

    def test_eliminar_manga_no_existe(self):
        response = client.delete("/mangas/delete/Nonexistent+Manga")
        self.assertEqual(response.status_code, 404)

    def test_lista_de_mangas(self):
        client.post("/mangas/add", json={"title": "The seven deadly sins", "author": "Nakaba Suzuki"})
        client.post("/mangas/add", json={"title":"Say the right thing", "author": "Kouji Seo"})
        response = client.get("/mangas/list")
        self.assertEqual(response.status_code, 200)
        mangalist = response.json()
        self.assertIn({"title": "The seven deadly sins", "author": "Nakaba Suzuki", "usuario_ultimo_prestamo": None}, mangalist)
        self.assertIn({"title": "Say the right thing", "author": "Kouji Seo", "usuario_ultimo_prestamo": None}, mangalist)

    def test_catalogo(self):
        client.delete("/mangas/reset")
        response = client.get("/mangas/list?catalogo=true")
        self.assertEqual(response.status_code, 200)
        mangalist = response.json()
        medida_inicial= len(mangalist)
        client.post("/prestamos/add", json={
            "titulo_manga": "Attack on titan",
            "email_usuario": "ancalderonj@unal.edu.co",
            "fecha": "2025-07-30"
        })
        response = client.get("/mangas/list?catalogo=true")
        self.assertEqual(response.status_code, 200)
        mangalist = response.json()
        self.assertEqual(len(mangalist), medida_inicial - 1)