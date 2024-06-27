import pandas as pd
import networkx as nx


def read_data():
    # Read the CSV file
    routes = pd.read_csv('./helper/path_finder/cleaned_data/routes_cleaned.csv')
    trips = pd.read_csv('./helper/path_finder/trains_data/trips_all_trains.txt')
    stop_times = pd.read_csv('./helper/path_finder/trains_data/stop_times_all_trains.txt')
    stops = pd.read_csv('./helper/path_finder/trains_data/stops_all_trains.txt')
    calendar_dates = pd.read_csv('./helper/path_finder/trains_data/calendar_dates_all_trains.txt')

    return routes, trips, stop_times, stops, calendar_dates

def create_graph(routes):
    G = nx.DiGraph()
    for index, row in routes.iterrows():
        route = [station.strip() for station in row['route_long_name'].split('|')]
        for i in range(len(route) - 1):
            G.add_edge(route[i], route[i+1],
                       route_long_name=row['route_long_name'],
                       route_id=row['route_id'])
    return G

def find_shortest_path(G, user_origin, user_destination):
    shortest_path = []
    if user_origin in G and user_destination in G:
        try:
            shortest_path = nx.shortest_path(G, source=user_origin, target=user_destination)
        except nx.NetworkXNoPath:
            print(f'No path found from {user_origin} to {user_destination}.')
    else:
        print(f'Either source {user_origin} or target {user_destination} is not in the graph.')
    return shortest_path

# def optimize_shortest_path(shortest_path, G):
    optimized_shortest_path = []
    current_route_id = None
    first_station = None
    last_station = None
    itinerary = []
    travel_optimization_details = []

    for i in range(len(shortest_path) - 1):
        edge_data = G.get_edge_data(shortest_path[i], shortest_path[i+1])

        if edge_data['route_id'] != current_route_id:
            if first_station is not None:
                optimized_shortest_path.append(last_station)
                itinerary.append({'start_station': first_station, 'end_station': last_station})

            current_route_id = edge_data['route_id']
            first_station = shortest_path[i]
            last_station = shortest_path[i+1]

        else:
            last_station = shortest_path[i+1]

        if first_station is not None:
            travel_optimization_details.append({'start_station': first_station, 'end_station': last_station, 'route_id': current_route_id})
            optimized_shortest_path.append(last_station)
            itinerary.append({'start_station': first_station, 'end_station': last_station})

    return optimized_shortest_path, itinerary, travel_optimization_details

def optimize_shortest_path(shortest_path, G):
    optimized_shortest_path = []
    current_route_id = None
    first_station = None
    last_station = None
    itinerary = []
    travel_optimization_details = []

    for i in range(len(shortest_path) - 1):
        edge_data = G.get_edge_data(shortest_path[i], shortest_path[i+1])

        if edge_data['route_id'] != current_route_id:
            if first_station is not None:
                itinerary.append({'start_station': first_station, 'end_station': last_station})
                travel_optimization_details.append({'start_station': first_station, 'end_station': last_station, 'route_id': current_route_id})
                optimized_shortest_path.append(last_station)

            current_route_id = edge_data['route_id']
            first_station = shortest_path[i]
            last_station = shortest_path[i+1]

        else:
            last_station = shortest_path[i+1]

    # Append the last station of the last route
    if last_station is not None:
        itinerary.append({'start_station': first_station, 'end_station': last_station})
        travel_optimization_details.append({'start_station': first_station, 'end_station': last_station, 'route_id': current_route_id})
        optimized_shortest_path.append(last_station)

    return optimized_shortest_path, itinerary, travel_optimization_details


def path_finder(origin, destination):
    routes, _, _, _, _ = read_data()
    G = create_graph(routes)
    shortest_path = find_shortest_path(G, origin, destination)
    optimized_shortest_path, itinerary, travel_optimization_details  = optimize_shortest_path(shortest_path, G)

    return {'optimized_shortest_path': optimized_shortest_path, 'itinerary': itinerary, 'travel_optimization_details': travel_optimization_details}
