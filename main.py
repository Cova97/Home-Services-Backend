from typing import Union, List
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.firebase_service import FirebaseService
from services.google_maps import GoogleMaps
from services.user_service import UserService
from services.messages_service import MessageService, MessageSend, MessageReceive

# Modelos Pydantic para las solicitudes
class UserCreateRequest(BaseModel):
    email: str
    password: str
    tipo_usuario: str  # 'cliente' o 'proveedor'
    direccion: str  # Dirección del usuario
    nombre: str  # Nombre del usuario
    apellido: str  # Apellido del usuario
    telefono: str  # Teléfono del usuario
    archivo_pdf: UploadFile = None  # Archivo PDF opcional para proveedores

class UserLoginRequest(BaseModel):
    email: str
    password: str
    rol_deseado: str  # 'cliente' o 'proveedor'

# Inicializar servicios
cred_path = 'serviceshomebackend-firebase.json'
firebase_service = FirebaseService(cred_path)
google_maps_service = GoogleMaps()
user_service = UserService(firebase_service.db, firebase_service)
message_service = MessageService(firebase_service.db)

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
async def crear_usuario(
    email: str = Form(...),
    password: str = Form(...),
    tipo_usuario: str = Form(...),
    direccion: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    telefono: str = Form(...),
    archivo_pdf: UploadFile = File(None)
):
    """
    Crea un nuevo usuario en Firebase Authentication y almacena información adicional en Firestore.
    Si el usuario ya existe, agrega el nuevo rol a la lista de roles.
    """
    if tipo_usuario not in ['cliente', 'proveedor']:
        raise HTTPException(status_code=400, detail="Tipo de usuario no válido. Debe ser 'cliente' o 'proveedor'.")

    try:
        # Geocodificar la dirección (obtener latitud y longitud)
        geocode_result = google_maps_service.get_geocode(direccion)
        if not geocode_result:
            raise HTTPException(status_code=400, detail="No se pudo geocodificar la dirección.")

        # Extraer latitud y longitud
        location = geocode_result[0]['geometry']['location']
        lat, lng = location['lat'], location['lng']

        # Crear el usuario
        user_uid = user_service.create_user(
            email=email,
            password=password,
            tipo_usuario=tipo_usuario,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            archivo_pdf=archivo_pdf,
            latitud=lat,
            longitud=lng
        )

        if user_uid:
            return {"message": "Usuario creado con éxito", "uid": user_uid}
        else:
            raise HTTPException(status_code=400, detail="Error al crear usuario.")
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
        user_record = firebase_service.get_user_by_email(user.email)
        
        # Obtener información adicional del usuario desde Firestore
        user_data = firebase_service.get_firestore_document('usuarios', user_record.uid)
        
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
    
# Ruta para enviar un mensaje
@app.post("/send-message", response_model=dict)
async def send_message(message: MessageSend):
    """
    Envía un mensaje de un usuario a otro.
    """
    # Aquí asumimos que el UID del remitente se pasa en el cuerpo de la solicitud.
    if not message_service.send_message(message.sender_uid, message.receiver_uid, message.text):
        raise HTTPException(status_code=400, detail="Error al enviar el mensaje")
    return {"message": "Mensaje enviado correctamente"}

# Ruta para obtener los mensajes recibidos
@app.get("/received-messages", response_model=List[MessageReceive])
async def get_received_messages(receiver_uid: str):
    """
    Obtiene todos los mensajes recibidos por un usuario.
    """
    messages = message_service.get_received_messages(receiver_uid)
    return messages

# Ruta para el chequeo de estado de la API HEALTCHECK
@app.get("/healthcheck")
def healthcheck():
    return {"message": "API en funcionamiento"}