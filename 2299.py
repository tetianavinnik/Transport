# # import csv

# # vehicle_id = "1915857"  # replace with the desired vehicle ID

# # with open(r'C:\Users\TETYANA\Desktop\Транспорт\data_4h.csv') as csvfile:
# #     reader = csv.DictReader(csvfile)
# #     for row in reader:
# #         if row['id'] == vehicle_id:
# #             bearing = float(row['bearing'])
# #             if bearing < 110 and bearing > 60:
# #                 timestamp = row['timestamp']
# #                 lat, long = row['latitude'], row['longitude']
# #                 print(f" {timestamp}||| {bearing}|||{lat}, {long}")


# import csv
# from math import atan, atan2, radians, cos, sin, sqrt

# # Function to calculate the distance between two points (latitude and longitude)
# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371000  # radius of Earth in meters
#     phi1 = radians(lat1)
#     phi2 = radians(lat2)
#     delta_phi = radians(lat2 - lat1)
#     delta_lambda = radians(lon2 - lon1)
#     a = sin(delta_phi/2)**2 + cos(phi1)*cos(phi2)*sin(delta_lambda/2)**2
#     c = 2*atan2(sqrt(a), sqrt(1 - a))
#     distance = R*c
#     print(distance)
#     return distance

# # Latitude and longitude of the stop
# stop_lat = 49.774093
# stop_lon = 24.012718

# # Threshold distance in meters
# distance_threshold = 200

# # Open the CSV file
# with open(r'C:\Users\TETYANA\Desktop\Транспорт\data_4h.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     lst = []
#     for row in reader:
#         if row['route_id'] == '1633' or row['route_id'] == '88' or row['route_id'] == '94' or row['route_id'] == '106':
#             # Latitude and longitude of the current bus
#             bus_lat = float(row['latitude'])
#             bus_lon = float(row['longitude'])
#             bearing = row["bearing"]
            
#             # Calculate the distance between the bus and the stop
#             distance = haversine(stop_lat, stop_lon, bus_lat, bus_lon)
            
#             # Check if the bus is within the threshold distance
#             if distance <= distance_threshold:
#                 lst += bearing
#                 print(f"Bus {row['vehicle_id']} was within {distance_threshold} meters of the stop at {bearing}, {bus_lat}, {bus_lon}")
#                 break
#                 # do something with the bus data here

#     print(max(lst), min(lst))


#AIzaSyBFHDMnkgT_RTdok4o4YDnPrnaynVEk0zg
import requests

def find_nearest_stop(latitude, longitude):
    # Define the API endpoint and parameters
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {'location': f'{latitude},{longitude}',
              'radius': 200,
              'type': 'transit_station',
              'key': 'AIzaSyBFHDMnkgT_RTdok4o4YDnPrnaynVEk0zg'}

    # Send the API request and get the response
    response = requests.get(url, params=params)
    data = response.json()

    # Extract the details of the nearest stop from the response
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return (str(lat) + "," + str(lng))
    # else:
    #     print('Error:', data['status'])
    #     return None


def func():
    with open(r"C:\Users\TETYANA\Desktop\transport\stops.txt", "r", encoding="utf-8") as f,\
        open(r"C:\Users\TETYANA\Desktop\transport\stops_corrected.txt", "a", encoding="utf-8") as f2:
        for stop in f:
            stop = stop.strip().split(',')
            # stop_name = "bus stop " + stop[2]
            lat, lon = stop[-2], stop[-1]
            coordinates = find_nearest_stop(lat, lon)
            print(coordinates)
            print(coordinates == None)
            if coordinates != None:
                f2.write(",".join(stop) + "," + coordinates + "\n")
            else:
                f2.write(",".join(stop) + "," + stop[-2] + "," + stop[-1] + "\n")


func()

