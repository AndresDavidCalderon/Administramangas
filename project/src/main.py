from fastapi import FastAPI
from .mangas import mangaRouter

app = FastAPI()
app.include_router(mangaRouter)


@app.get("/")
def read_root():
    return {"Hello": "World"}