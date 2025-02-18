from firebase_admin import auth

class UserService:
    def __init__(self, db, firebase_service):
        """
        Inicializa UserService con una instancia de Firestore y FirebaseService.

        :param db: Instancia de Firestore.
        :param firebase_service: Instancia de FirebaseService.
        """
        self.db = db
        self.firebase_service = firebase_service

    def create_user(self, email, password, tipo_usuario, nombre, apellido, telefono, direccion=None, archivo_pdf=None):
        """
        Crea un nuevo usuario en Firebase Authentication y almacena información adicional en Firestore.
        Si el usuario ya existe, agrega el nuevo rol a la lista de roles.

        :param email: Correo electrónico del usuario.
        :param password: Contraseña del usuario.
        :param tipo_usuario: Tipo de usuario ('cliente' o 'proveedor').
        :param nombre: Nombre del usuario.
        :param apellido: Apellido del usuario.
        :param telefono: Teléfono del usuario.
        :param direccion: Dirección del usuario (opcional).
        :param archivo_pdf: Archivo PDF para proveedores (opcional).
        :return: UID del usuario creado o None si hay un error.
        """
        if tipo_usuario not in ['cliente', 'proveedor']:
            print("Tipo de usuario no válido. Debe ser 'cliente' o 'proveedor'.")
            return None

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
                user_uid = self.firebase_service.create_user(email, password)
                
                user_data = {
                    'email': email,
                    'tipo_usuario': [tipo_usuario],  # Almacenar el rol como una lista
                    'nombre': nombre,
                    'apellido': apellido,
                    'telefono': telefono
                }

                # Si el usuario es un proveedor, subir el archivo PDF y almacenar la URL
                if tipo_usuario == 'proveedor' and archivo_pdf:
                    pdf_url = self.firebase_service.upload_file_to_storage(archivo_pdf, f"proveedores/{user_uid}/documento.pdf")
                    if pdf_url:
                        user_data['pdf_url'] = pdf_url
                    else:
                        print("Error al subir el archivo PDF.")
                
                # Si el usuario es un proveedor o cliente, almacenar la dirección
                if tipo_usuario == 'proveedor' or tipo_usuario == 'cliente':
                    user_data['direccion'] = direccion
                
                # Guardar los datos del usuario en Firestore
                self.db.collection('usuarios').document(user_uid).set(user_data)
                print(f"Usuario registrado con éxito: {user_uid}")
                return user_uid
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return None