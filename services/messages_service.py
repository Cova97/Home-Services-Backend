from firebase_admin import firestore
from fastapi import HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Modelo Pydantic para enviar mensajes
class MessageSend(BaseModel):
    sender_uid: str  # UID del usuario que envía el mensaje
    receiver_uid: str  # UID del usuario que recibe el mensaje
    text: str  # Contenido del mensaje
    
# Modelo Pydantic para recibir mensajes
class MessageReceive(BaseModel):
    sender_uid: str    # UID del usuario que envía el mensaje
    text: str          # Contenido del mensaje
    timestamp: str     # Fecha y hora del mensaje

class MessageService:
    def __init__(self, db):
        """
        Inicializa el servicio de mensajes con una instancia de Firestore.

        :param db: Instancia de Firestore.
        """
        self.db = db

    def send_message(self, sender_uid: str, receiver_uid: str, text: str):
        """
        Envía un mensaje de un usuario a otro.

        :param sender_uid: UID del usuario que envía el mensaje.
        :param receiver_uid: UID del usuario que recibe el mensaje.
        :param text: Contenido del mensaje.
        :return: True si el mensaje se envió correctamente, False si hubo un error.
        """
        try:
            # Crear el mensaje en Firestore
            message_data = {
                "sender_uid": sender_uid,
                "receiver_uid": receiver_uid,
                "text": text,
                "timestamp": firestore.SERVER_TIMESTAMP
            }

            # Guardar el mensaje en la colección "messages"
            self.db.collection("messages").add(message_data)
            return True
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            return False

    def get_received_messages(self, receiver_uid: str):
        """
        Obtiene todos los mensajes recibidos por un usuario.

        :param receiver_uid: UID del usuario que recibe los mensajes.
        :return: Lista de mensajes recibidos.
        """
        try:
            # Obtener los mensajes donde el usuario actual es el receptor
            messages_ref = self.db.collection("messages").where("receiver_uid", "==", receiver_uid)
            messages = messages_ref.stream()

            # Formatear los mensajes
            received_messages = []
            for message in messages:
                message_data = message.to_dict()
                received_messages.append(MessageReceive(
                    sender_uid=message_data["sender_uid"],
                    text=message_data["text"],
                    timestamp=message_data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                ))

            return received_messages
        except Exception as e:
            print(f"Error al obtener mensajes recibidos: {e}")
            return []