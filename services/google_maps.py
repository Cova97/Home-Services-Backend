import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleMaps:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.client = googlemaps.Client(key=self.api_key)

    def get_geocode(self, address):
        """
        Obtiene la geocodificación de una dirección.

        :param address: Dirección a geocodificar.
        :return: Resultado de la geocodificación o None si hay un error.
        """
        try:
            geocode = self.client.geocode(address)
            return geocode
        except Exception as e:
            print(f"Error al obtener geocodificación: {e}")
            return None

    def get_distance(self, origin, destination):
        """
        Obtiene la distancia entre dos ubicaciones.

        :param origin: Ubicación de origen.
        :param destination: Ubicación de destino.
        :return: Resultado de la matriz de distancia o None si hay un error.
        """
        try:
            distance = self.client.distance_matrix(origin, destination)
            return distance
        except Exception as e:
            print(f"Error al obtener distancia: {e}")
            return None