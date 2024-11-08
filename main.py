import os
from db_utils import Neo4jDB,print_closest_hotel_info
from map_utils import generate_paths, plot_map
from point_utils import latitude_Start,longitude_Start, get_target_point

def main():
    OS_PATH = os.path.dirname(os.path.realpath(__file__))
    print(OS_PATH)

    # Définissez vos coordonnées url, userName et password ici
    url = "bolt://localhost:7687"
    username = "TEST_Project"
    password = "123456789"

    # Initialiser l'objet Neo4jDB
    neo4j_db = Neo4jDB(url, username, password)

    # Récupérer le point de départ
    origin_point = (latitude_Start,longitude_Start)

    # Récupérer le point d'arrivée en utilisant la fonction find_closest_hotel
    closest_hotel = neo4j_db.find_closest_hotel(origin_point[0], origin_point[1])
    target_point = get_target_point(closest_hotel)
    print_closest_hotel_info(closest_hotel)

    print("Origin Point:", origin_point)
    print("Target Point:", target_point)

    perimeter = 0.5
    k = 1

    print("* * * * * * * * * * * * * Finding Optimal Paths * * * * * * * * * * * * * *")
    paths = generate_paths(origin_point, target_point, perimeter, k)
    plot_map(origin_point, target_point, paths, k, OS_PATH)

if __name__ == "__main__":
    main()
