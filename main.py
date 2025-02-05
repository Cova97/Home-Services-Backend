from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, auth, firestore
from pydantic import BaseModel

# Modelos Pydantic para las solicitudes
class UserCreateRequest(BaseModel):
    email: str
    password: str
    tipo_usuario: str  # 'cliente' o 'proveedor'

class UserLoginRequest(BaseModel):
    email: str
    password: str

# Inicializar Firebase
cred_path = 'serviceshomebackend-firebase.json'
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Inicializar Firestore
db = firestore.client()

# Configuración de FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las peticiones
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todas las cabeceras
)

# Ruta para crear un usuario
@app.post("/crear-usuario")
def crear_usuario(user: UserCreateRequest):
    """
    Crea un nuevo usuario en Firebase Authentication y almacena información adicional en Firestore.
    """
    if user.tipo_usuario not in ['cliente', 'proveedor']:
        raise HTTPException(status_code=400, detail="Tipo de usuario no válido. Debe ser 'cliente' o 'proveedor'.")

    try:
        # Crear el usuario en Firebase Authentication
        user_record = auth.create_user(
            email=user.email,
            password=user.password
        )
        
        # Guardar información adicional en Firestore
        user_data = {
            'email': user.email,
            'tipo_usuario': user.tipo_usuario
        }
        
        db.collection('usuarios').document(user_record.uid).set(user_data)
        
        return {"message": "Usuario creado con éxito", "uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear usuario: {str(e)}")

# Ruta para autenticar un usuario y obtener su tipo
@app.post("/login")
def login(user: UserLoginRequest):
    """
    Autentica un usuario y devuelve su tipo (cliente o proveedor).
    """
    try:
        # Autenticar al usuario (esto normalmente lo haría el cliente)
        # Aquí simulamos la autenticación obteniendo el usuario por email
        user_record = auth.get_user_by_email(user.email)
        
        # Obtener información adicional del usuario desde Firestore
        user_ref = db.collection('usuarios').document(user_record.uid)
        user_data = user_ref.get().to_dict()
        
        if user_data:
            return {
                "message": "Autenticación exitosa",
                "uid": user_record.uid,
                "email": user.email,
                "tipo_usuario": user_data['tipo_usuario']
            }
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en Firestore")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al autenticar usuario: {str(e)}")

# Ruta de prueba
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Ruta de ejemplo
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}