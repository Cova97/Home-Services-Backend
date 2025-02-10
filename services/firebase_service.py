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
        Si el usuario ya existe, agrega el nuevo rol a la lista de roles.

        :param email: Correo electrónico del usuario.
        :param password: Contraseña del usuario.
        :param tipo_usuario: Tipo de usuario ('cliente' o 'proveedor').
        :return: UID del usuario registrado o None si hay un error.
        """
        try:
            # Verificar si el usuario ya existe en Firestore
            user_query = self.db.collection('usuarios').where('email', '==', email).limit(1).get()
            
            if user_query:
                # Si el usuario ya existe, obtener sus datos
                user_doc = user_query[0]
                user_data = user_doc.to_dict()
                user_uid = user_doc.id

                # Verificar si el usuario ya tiene el rol que se está intentando registrar
                if 'tipo_usuario' in user_data and tipo_usuario in user_data['tipo_usuario']:
                    print(f"El usuario ya tiene el rol de {tipo_usuario}.")
                    return None

                # Si no tiene el rol, agregarlo a la lista de roles
                if 'tipo_usuario' not in user_data:
                    user_data['tipo_usuario'] = []
                user_data['tipo_usuario'].append(tipo_usuario)

                # Actualizar el documento en Firestore
                self.db.collection('usuarios').document(user_uid).update(user_data)
                print(f"Rol {tipo_usuario} agregado al usuario {user_uid}.")
                return user_uid
            else:
                # Si el usuario no existe, crear uno nuevo
                user = auth.create_user(
                    email=email,
                    password=password
                )
                
                user_data = {
                    'email': email,
                    'tipo_usuario': [tipo_usuario]  # Almacenar el rol como una lista
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