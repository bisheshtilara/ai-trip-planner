import csv
import networkx as nx

# Fonction pour construire le graphe pondéré à partir des données
def construire_graphe(routes_file, stops_file, trips_file):
    G = nx.DiGraph()
    
    # Lire les fichiers routes_cleaned.csv et ajouter les arrêts au graphe
    with open(routes_file, newline='', encoding='utf-8') as routes_csv:
        routes_reader = csv.reader(routes_csv)
        next(routes_reader)  # Ignorer l'en-tête
        for row in routes_reader:
            route_id, _, _, route_long_name, _ = row
            stops = route_long_name.split('|')
            for i in range(len(stops) - 1):
                G.add_edge(stops[i], stops[i+1], weight=1)  # Poids arbitraire ici

# Lire les fichiers stops_times_all_trains.txt et ajouter les horaires au graphe
    with open(stops_file, newline='', encoding='utf-8') as stops_txt:
        stops_reader = csv.reader(stops_txt, delimiter=',')
        next(stops_reader)  # Ignorer l'en-tête
        for row in stops_reader:
            trip_id, _, arrival_time_str, stop_id, _, _, _, _, _ = row
            if stop_id in G:
                G.nodes[stop_id][trip_id] = arrival_time_str
            else:
                print(f"Le nœud {stop_id} n'existe pas dans le graphe.")


    # Lire les fichiers trips_all_trains.txt et ajouter les voyages au graphe
    with open(trips_file, newline='', encoding='utf-8') as trips_txt:
        trips_reader = csv.reader(trips_txt, delimiter=',')
        next(trips_reader)  # Ignorer l'en-tête
        for row in trips_reader:
            _, _, trip_id, trip_headsign, _, _, _ = row
            trip_stops = trip_headsign.split('|')
            for i in range(len(trip_stops) - 1):
                G.add_edge(trip_stops[i], trip_stops[i+1], trip_id=trip_id)

    return G

# Construire le graphe à partir des fichiers
routes_file = 'data_sncf_all_trains/routes_cleaned.csv'
stops_file = 'data_sncf_all_trains/stop_times_all_trains.txt'
trips_file = 'data_sncf_all_trains/trips_all_trains.txt'
graphe = construire_graphe(routes_file, stops_file, trips_file)

# Utiliser l'algorithme de Floyd-Warshall pour trouver tous les plus courts chemins entre chaque paire de nœuds
plus_courts_chemins = nx.floyd_warshall(graphe, weight='weight')

# Exemple d'utilisation : trouver le plus court chemin entre deux nœuds
depart = 'Lille'
arrivee = 'Paris'
if depart in plus_courts_chemins and arrivee in plus_courts_chemins[depart]:
    chemin_longueur = plus_courts_chemins[depart][arrivee]
    print("Longueur du chemin le plus court:", chemin_longueur)
    chemin = nx.shortest_path(graphe, source=depart, target=arrivee)
    print("Chemin:", chemin)
else:
    print("Aucun chemin trouvé entre les points spécifiés.")
