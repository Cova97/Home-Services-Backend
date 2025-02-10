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
    rol_deseado: str # 'cliente' o 'proveedor'

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
    Si el usuario ya existe, agrega el nuevo rol a la lista de roles.
    """
    if user.tipo_usuario not in ['cliente', 'proveedor']:
        raise HTTPException(status_code=400, detail="Tipo de usuario no válido. Debe ser 'cliente' o 'proveedor'.")

    try:
        # Verificar si el usuario ya existe en Firestore
        user_query = db.collection('usuarios').where('email', '==', user.email).limit(1).get()
        
        if user_query:
            # Si el usuario ya existe, obtener sus datos
            user_doc = user_query[0]
            user_data = user_doc.to_dict()
            user_uid = user_doc.id

            # Verificar si el usuario ya tiene el rol que se está intentando registrar
            if 'tipo_usuario' in user_data and user.tipo_usuario in user_data['tipo_usuario']:
                raise HTTPException(status_code=400, detail=f"El usuario ya tiene el rol de {user.tipo_usuario}.")

            # Si no tiene el rol, agregarlo a la lista de roles
            if 'tipo_usuario' not in user_data:
                user_data['tipo_usuario'] = []
            user_data['tipo_usuario'].append(user.tipo_usuario)

            # Actualizar el documento en Firestore
            db.collection('usuarios').document(user_uid).update(user_data)
            return {"message": f"Rol {user.tipo_usuario} agregado al usuario {user_uid}."}
        else:
            # Si el usuario no existe, crear uno nuevo
            user_record = auth.create_user(
                email=user.email,
                password=user.password
            )
            
            user_data = {
                'email': user.email,
                'tipo_usuario': [user.tipo_usuario]  # Almacenar el rol como una lista
            }
            
            db.collection('usuarios').document(user_record.uid).set(user_data)
            return {"message": "Usuario creado con éxito", "uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear usuario: {str(e)}")

# Ruta para autenticar un usuario y obtener su tipo
@app.post("/login")
def login(user: UserLoginRequest):
    """
    Autentica un usuario y verifica si tiene el rol deseado.
    """
    try:
        # Autenticar al usuario (esto normalmente lo haría el cliente)
        # Aquí simulamos la autenticación obteniendo el usuario por email
        user_record = auth.get_user_by_email(user.email)
        
        # Obtener información adicional del usuario desde Firestore
        user_ref = db.collection('usuarios').document(user_record.uid)
        user_data = user_ref.get().to_dict()
        
        if user_data:
            # Verificar si el usuario tiene el rol deseado
            if 'tipo_usuario' in user_data and user.rol_deseado in user_data['tipo_usuario']:
                return {
                    "message": f"Autenticación exitosa como {user.rol_deseado}",
                    "uid": user_record.uid,
                    "email": user.email,
                    "tipo_usuario": user.rol_deseado
                }
            else:
                raise HTTPException(
                    status_code=403,
                    detail=f"El usuario no tiene el rol de {user.rol_deseado}. Roles disponibles: {user_data['tipo_usuario']}"
                )
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