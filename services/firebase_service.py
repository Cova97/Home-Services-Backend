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

    def create_user(self, email, password):
        """
        Crea un nuevo usuario en Firebase Authentication.

        :param email: Correo electrónico del usuario.
        :param password: Contraseña del usuario.
        :return: UID del usuario creado o None si hay un error.
        """
        try:
            user = auth.create_user(email=email, password=password)
            return user.uid
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return None

    def get_user_by_email(self, email):
        """
        Obtiene un usuario por su correo electrónico.

        :param email: Correo electrónico del usuario.
        :return: Usuario o None si hay un error.
        """
        try:
            user = auth.get_user_by_email(email)
            return user
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def verify_id_token(self, token):
        """
        Verifica el token de autenticación.

        :param token: Token de autenticación.
        :return: Diccionario con la información del token o None si hay un error.
        """
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception as e:
            print(f"Error al verificar token: {e}")
            return None

    def get_firestore_document(self, collection, document_id):
        """
        Obtiene un documento de Firestore.

        :param collection: Nombre de la colección.
        :param document_id: ID del documento.
        :return: Diccionario con los datos del documento o None si hay un error.
        """
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                return None
        except Exception as e:
            print(f"Error al obtener documento de Firestore: {e}")
            return None

    def set_firestore_document(self, collection, document_id, data):
        """
        Establece un documento en Firestore.

        :param collection: Nombre de la colección.
        :param document_id: ID del documento.
        :param data: Datos a almacenar en el documento.
        :return: True si se guardó correctamente, False si hubo un error.
        """
        try:
            self.db.collection(collection).document(document_id).set(data)
            return True
        except Exception as e:
            print(f"Error al establecer documento en Firestore: {e}")
            return False

    def update_firestore_document(self, collection, document_id, data):
        """
        Actualiza un documento en Firestore.

        :param collection: Nombre de la colección.
        :param document_id: ID del documento.
        :param data: Datos a actualizar en el documento.
        :return: True si se actualizó correctamente, False si hubo un error.
        """
        try:
            self.db.collection(collection).document(document_id).update(data)
            return True
        except Exception as e:
            print(f"Error al actualizar documento en Firestore: {e}")
            return False