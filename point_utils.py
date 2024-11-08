
latitude_Start = 34.031464
longitude_Start = -4.985343
#pointA_latitude =34.031464
#pointA_longitude =-4.985343

def get_target_point(hotel_proche):
    # Vous pouvez ajouter ici la logique pour récupérer le point d'arrivée depuis une source externe
    return (hotel_proche["Latitude"], hotel_proche["Longitude"])  # Utilisation des coordonnées de l'hôtel le plus proche
