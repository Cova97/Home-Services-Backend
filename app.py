from services.user_service import UserService
import firebase_admin
from firebase_admin import credentials, firestore

def prueba_firestore(db):
    """
    Prueba mínima para verificar la conexión a Firestore.
    Intenta escribir un documento en una colección de prueba.
    """
    try:
        # Intentar escribir un documento en Firestore
        doc_ref = db.collection('prueba').document('doc1')
        doc_ref.set({
            'campo1': 'valor1',
            'campo2': 'valor2'
        })
        print("Documento escrito correctamente en Firestore.")
    except Exception as e:
        print(f"Error al escribir en Firestore: {e}")

def main():
    # Ruta al archivo de credenciales de Firebase
    cred_path = 'serviceshomebackend-firebase.json'
    
    # Inicializar Firebase solo una vez
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    
    # Inicializar Firestore
    db = firestore.client()
    
    # Prueba mínima de Firestore
    print("Probando conexión a Firestore...")
    prueba_firestore(db)
    
    # Crear una instancia de UserService y pasarle la instancia de Firestore
    user_service = UserService(db)
    
    # Crear un usuario de tipo 'cliente'
    print("\nCreando usuario de tipo 'cliente'...")
    cliente_uid = user_service.crear_usuario('cliente4@example.com', 'password123', 'cliente')
    
    # Crear un usuario de tipo 'proveedor'
    print("\nCreando usuario de tipo 'proveedor'...")
    proveedor_uid = user_service.crear_usuario('proveedor4@example.com', 'password123', 'proveedor')

if __name__ == "__main__":
    main()