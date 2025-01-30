from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuracion de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permitir todas las peticiones
    allow_credentials=True,
    allow_methods=["*"], # Permitir todos los metodos
    allow_headers=["*"], # Permitir todas las cabeceras
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}