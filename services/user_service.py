from firebase_admin import auth

class UserService:
    def __init__(self, db):
        """
        Inicializa UserService con una instancia de Firestore.

        :param db: Instancia de Firestore.
        """
        self.db = db

    def crear_usuario(self, email, password, tipo_usuario):
        """
        Crea un nuevo usuario en Firebase Authentication y almacena información adicional en Firestore.

        :param email: Correo electrónico del usuario.
        :param password: Contraseña del usuario.
        :param tipo_usuario: Tipo de usuario ('cliente' o 'proveedor').
        :return: UID del usuario creado o None si hay un error.
        """
        if tipo_usuario not in ['cliente', 'proveedor']:
            print("Tipo de usuario no válido. Debe ser 'cliente' o 'proveedor'.")
            return None

        try:
            # Crear el usuario en Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password
            )
            
            # Guardar información adicional en Firestore
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