import csv
from datetime import time
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

    # Convertir une chaîne de caractères représentant l'heure en un objet time
    def convertir_heure(heure_str, line_number):
        try:
            heures, minutes, secondes = heure_str.split(':')
            # Vérifier si les heures sont dans la plage valide (0-23)
            if 0 <= int(heures) <= 23 and 0 <= int(minutes) < 60 and 0 <= int(secondes) < 60:
                return time(int(heures), int(minutes), int(secondes))
            else:
                print(f"L'heure n'est pas valide sur la ligne {line_number}: {heure_str}")
                return None
        except ValueError:
            print(f"L'heure n'est pas valide sur la ligne {line_number}: {heure_str}")
            return None

    # Lire les fichiers stops_times_all_trains.txt et ajouter les horaires au graphe
    with open(stops_file, newline='', encoding='utf-8') as stops_txt:
        stops_reader = csv.reader(stops_txt, delimiter=',')
        next(stops_reader)  # Ignorer l'en-tête
        for line_number, row in enumerate(stops_reader, start=2):  # Commencer à 2 pour inclure l'en-tête
            trip_id, arrival_time_str, _, _, _, _, _, _, _ = row
            arrival_time = convertir_heure(arrival_time_str, line_number)
            if arrival_time is not None:
                # Ajouter les horaires au graphe en utilisant trip_id comme clé
                for node in G.nodes:
                    G.nodes[node][trip_id] = arrival_time

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

# Fonction pour trouver le chemin le plus court entre deux points en utilisant l'algorithme de Bellman-Ford
def trouver_chemin_plus_court(graphe, depart, arrivee):
    try:
        chemin = nx.bellman_ford_path(graphe, source=depart, target=arrivee, weight='weight')
        return chemin
    except nx.NetworkXNoPath:
        print("Aucun chemin trouvé entre les points spécifiés.")
        return None

# Exemple d'utilisation
routes_file = 'data_sncf_all_trains/routes_cleaned.csv'
stops_file = 'data_sncf_all_trains/stop_times_all_trains.txt'
trips_file = 'data_sncf_all_trains/trips_all_trains.txt'

graphe = construire_graphe(routes_file, stops_file, trips_file)
depart = 'Paris'
arrivee = 'Montaigne'
chemin = trouver_chemin_plus_court(graphe, depart, arrivee)
print("Chemin le plus court:", chemin)

