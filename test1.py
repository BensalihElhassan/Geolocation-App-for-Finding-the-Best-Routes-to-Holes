from neo4j import GraphDatabase

# Définir les coordonnées du point A
pointA_latitude = 34.031464
pointA_longitude = -4.985343

# Informations d'accès à la base de données Neo4j
url = "bolt://localhost:7687"
userName = "TEST_Project"
password = "123456789"

# Requête Cypher pour trouver l'hôtel le plus proche du point A
cql_query = (
    "WITH point({latitude: $latitude, longitude: $longitude}) AS pointA "
    "MATCH (h:HOTEL) "
    "WITH pointA, h, point({latitude: h.latitude, longitude: h.longitude}) AS hotelPoint "
    "RETURN h.name AS Nom, h.latitude AS Latitude, h.longitude AS Longitude, "
    "point.distance(pointA, hotelPoint) AS distance "
    "ORDER BY distance LIMIT 1"
)

# Connexion à la base de données Neo4j
graphDB_Driver = GraphDatabase.driver(url, auth=(userName, password))

# Exécution de la requête Cypher et récupération des résultats
with graphDB_Driver.session() as graphDB_Session:
    result = graphDB_Session.run(cql_query, latitude=pointA_latitude, longitude=pointA_longitude)
    closest_hotel = result.single()  # Récupérer le premier et unique résultat

# Vérifier s'il y a un hôtel trouvé
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
#***********************************************************

import os
import networkx as nx
import plotly.graph_objects as go
import osmnx as ox
import time


def k_shortest_paths(graph, start_node, end_node, k):
    paths = list(nx.all_shortest_paths(graph, source=start_node, target=end_node, method='dijkstra'))
    return paths[:k] if len(paths) >= k else paths


def generate_paths(origin_point, target_point, perimeter, k):
    origin_lat, origin_long = origin_point
    target_lat, target_long = target_point

    north, south = max(origin_lat, target_lat), min(origin_lat, target_lat)
    east, west = max(origin_long, target_long), min(origin_long, target_long)

    mode = 'drive'
    roadgraph = ox.graph_from_bbox(north + perimeter, south - perimeter, east + perimeter, west - perimeter,network_type=mode, simplify=True)

    origin_coords = (origin_long, origin_lat)
    target_coords = (target_long, target_lat)

    origin_node = ox.distance.nearest_nodes(roadgraph, *origin_coords)
    target_node = ox.distance.nearest_nodes(roadgraph, *target_coords)

    start_time = time.time()
    routes = k_shortest_paths(roadgraph, origin_node, target_node, k)
    elapsed_time = time.time() - start_time
    print(f"Time elapsed for finding {k} shortest paths: {elapsed_time} seconds")

    paths = []
    for i, route in enumerate(routes):
        lat_long = [(roadgraph.nodes[node_id]['y'], roadgraph.nodes[node_id]['x']) for node_id in route]
        lat, long = zip(*lat_long)
        paths.append((long, lat, i))

    return paths


def plot_map(origin_point, target_point, paths, k):
    print("Setting up figure...")
    fig = go.Figure()

    # Plotting origin and target points
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=[origin_point[1]],
        lat=[origin_point[0]],
        marker={'size': 16, 'color': '#CE55FF'},
        name="Origin"
    ))

    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=[target_point[1]],
        lat=[target_point[0]],
        marker={'size': 16, 'color': '#CE55FF'},
        name="Destination"
    ))

    # Plotting each path with a different color
    colors = ['#FF0000', '#0000FF', '#00FF00'][:k]
    for i, path in enumerate(paths):
        long, lat, color_index = path
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=long,
            lat=lat,
            marker={'size': 10},
            name=f"Path {i + 1}",
            line=dict(width=4.5, color=colors[color_index]),
        ))

    # Map layout settings
    fig.update_layout(
        mapbox_style="mapbox://styles/mapbox/satellite-v9",
        # mapbox_style="mapbox://styles/mapbox/outdoors-v12",
        mapbox_accesstoken="pk.eyJ1IjoiZWxoc3NhbmFuaXIiLCJhIjoiY2x2bWdiZ2xwMDF0bjJpbzFiaG1lbThydSJ9.GdYHaG3ukcuyMSubvAbHLQ",
        legend=dict(yanchor="top", y=1, xanchor="left", x=0.83),
        # title=f"<span style='font-size: 32px;'><b>The K Shortest Paths Map ({k} Paths)</b></span>",
        font_family="Times New Roman",
        font_color="#333333",
        title_font_size=32,
        font_size=18,
        width=2000,
        height=1000,
    )

    # Set the center of the map
    lat_center = (origin_point[0] + target_point[0]) / 2
    long_center = (origin_point[1] + target_point[1]) / 2

    # Add the center to the map layout
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        title=dict(yanchor="top", y=.97, xanchor="left", x=0.03),
        mapbox={
            'center': {'lat': lat_center, 'lon': long_center},
            'zoom': 12.2
        }
    )

    print("Saving image to the output folder...")
    fig.write_image(os.path.join(OS_PATH, 'output', f'K_Shortest_Paths_Map2_{k}.jpg'), scale=3)
    print("Generating the map in the browser...")
    fig.show()


# Code starts here
OS_PATH = os.path.dirname(os.path.realpath(__file__))
print(OS_PATH)
# pointA_latitude = 34.031464
# pointA_longitude = -4.985343
# User input validation
while True:
    try:
        # origin_input = input("Enter the origin geocoordinate (latitude, longitude): ")
        # target_input = input("Enter the target geocoordinate (latitude, longitude): ")
        # Récupération des coordonnées de l'origine et de la cible
        origin_point = (pointA_latitude, pointA_longitude)
        target_point = (hotel_proche["Latitude"],  hotel_proche["Longitude"])

        print("Origin Point:", origin_point)
        print("Target Point:", target_point)

        break
    except ValueError:
        print("Invalid input. Please enter valid latitude and longitude.")

# Perimeter value
perimeter = 0.5

# Number of paths to find
k = 1

# Generate and plot paths
print("* * * * * * * * * * * * * Finding Optimal Paths * * * * * * * * * * * * * *")
paths = generate_paths(origin_point, target_point, perimeter, k)
plot_map(origin_point, target_point, paths, k)



