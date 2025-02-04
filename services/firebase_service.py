import firebase_admin
from firebase_admin import credentials, auth, firestore

class FirebaseService:
    def __init__(self, cred_path):
        """
        Inicializa FirebaseService con la ruta al archivo de credenciales de Firebase.

        :param cred_path: Ruta al archivo JSON de credenciales de Firebase.
        """
        self.cred_path = cred_path
        self.initialize_firebase()
        self.db = firestore.client()

    def initialize_firebase(self):
        """
        Inicializa la aplicación Firebase con las credenciales proporcionadas.
        """
        try:
            cred = credentials.Certificate(self.cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase inicializado correctamente.")
        except Exception as e:
            print(f"Error al inicializar Firebase: {e}")

    def registrar_usuario(self, email, password, tipo_usuario):
        """
        Registra un nuevo usuario en Firebase Authentication y almacena información adicional en Firestore.

        :param email: Correo electrónico del usuario.
        :param password: Contraseña del usuario.
        :param tipo_usuario: Tipo de usuario ('cliente' o 'proveedor').
        :return: UID del usuario registrado o None si hay un error.
        """
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            
            user_data = {
                'email': email,
                'tipo_usuario': tipo_usuario
            }
            
            self.db.collection('usuarios').document(user.uid).set(user_data)
            
            print(f"Usuario registrado con éxito: {user.uid}")
            return user.uid
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return None

    def iniciar_sesion(self, token):
        """
        Verifica el token de autenticación y obtiene la información del usuario desde Firestore.

        :param token: Token de autenticación generado por el cliente.
        :return: Diccionario con la información del usuario o None si hay un error.
        """
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            
            user_ref = self.db.collection('usuarios').document(uid)
            user_data = user_ref.get().to_dict()
            
            if user_data:
                print(f"Usuario autenticado: {uid}")
                return user_data
            else:
                print("Usuario no encontrado en Firestore")
                return None
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return None