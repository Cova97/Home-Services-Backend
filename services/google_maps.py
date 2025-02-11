import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleMaps:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.client = googlemaps.Client(key=self.api_key)

    def get_geocode(self, address):
        geocode = self.client.geocode(address)
        return geocode

    def get_distance(self, origin, destination):
        distance = self.client.distance_matrix(origin, destination)
        return distance

    def capture_address(self, user_id, address):
        # Obtener la geocodificación de la dirección
        geocode_result = self.get_geocode(address)
        
        if geocode_result:
            # Extraer latitud y longitud
            location = geocode_result[0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            
            # Almacenar la dirección en Firestore
            user_ref = self.db.collection('users').document(user_id)
            user_ref.set({
                'address': address,
                'location': {
                    'lat': lat,
                    'lng': lng
                }
            }, merge=True)
            
            return True
        else:
            return False


if __name__ == '__main__':       
    # caso de uso para obtener la geocodificación de una dirección
    maps = GoogleMaps()
    geocode = maps.get_geocode('Privada Abasolo, Num.4, Col. San Lorenzo Almecatla, 72710, Cuautlancingo, Pue.')

    # que solo me imprima la latitud y longitud
    location = geocode[0]['geometry']['location']
    lat = location['lat']
    lng = location['lng']

    print(lat, lng)

