from pydantic import BaseModel

class Manga(BaseModel):
    pass


def anadir_manga(client, title, author):
    response = client.post("/mangas/add", json={"title": title, "author": author})
    return response