from neo4j import GraphDatabase
from point_utils import latitude_Start, longitude_Start

class Neo4jDB:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.driver = GraphDatabase.driver(self.url, auth=(self.username, self.password))

    def find_closest_hotel(self, point_latitude, point_longitude):
        cql_query = (
            "WITH point({latitude: $latitude_Start, longitude: $longitude_Start}) AS pointA "
            "MATCH (h:HOTEL) "
            "WITH pointA, h, point({latitude: h.latitude, longitude: h.longitude}) AS hotelPoint "
            "RETURN h.name AS Nom, h.latitude AS Latitude, h.longitude AS Longitude, "
            "point.distance(pointA, hotelPoint) AS distance "
            "ORDER BY distance LIMIT 1"
        )

        with self.driver.session() as session:
            result = session.run(cql_query, latitude_Start=point_latitude, longitude_Start=point_longitude)
            closest_hotel = result.single()

        return closest_hotel

def print_closest_hotel_info(closest_hotel):
    if closest_hotel:
        # Récupérer les informations de l'hôtel le plus proche
        nom_hotel = closest_hotel["Nom"]
        latitude_hotel = closest_hotel["Latitude"]
        longitude_hotel = closest_hotel["Longitude"]
        distance_hotel = closest_hotel["distance"]

        # Stocker les informations dans une variable Python
        hotel_proche = {
            "Nom": nom_hotel,
            "Latitude": latitude_hotel,
            "Longitude": longitude_hotel,
            "Distance": distance_hotel
        }

        # Afficher les informations de l'hôtel le plus proche
        print("L'hôtel le plus proche est :", hotel_proche)
    else:
        print("Aucun hôtel trouvé proche du point A.")