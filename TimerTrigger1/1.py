# import datetime
import logging

import azure.functions as func

import requests
# import gtfs_realtime_pb2_lib
from google.transit import gtfs_realtime_pb2
import pyodbc


def get_vehicles():
    logging.info('Fetching vehicles')
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://track.ua-gis.com/gtfs/lviv/vehicle_position')
    feed.ParseFromString(response.content)
    return feed.entity


def upload_vehicle_positions_into_database(vehicles):
    logging.info('Starting upload')
    cnxn = pyodbc.connect(f"Server=tcp:lvivtransportserver.database.windows.net,1433;Initial Catalog=lvivtransportdb;Persist Security Info=False;User ID=codelvivtransport;Password=C0delvivtransport;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;")
    cursor = cnxn.cursor()
    # cursor.execute("BEGIN TRANSACTION;")
    for vehicle in vehicles:
        logging.info('Writing vehicle with id=%s', vehicle.vehicle.vehicle.id)
        cursor.execute(f'INSERT INTO vehicle_data (id,trip_id,route_id,schedule_relationship,vehicle_id,license_plate,latitude,longitude,bearing,odometer,speed,timestamp,congestion_level) VALUES ({vehicle.id}, {vehicle.vehicle.trip.trip_id}, {vehicle.vehicle.trip.route_id}, {vehicle.vehicle.trip.schedule_relationship},\
                   {vehicle.vehicle.vehicle.id}, {vehicle.vehicle.vehicle.license_plate}, {vehicle.vehicle.position.latitude}, {vehicle.vehicle.position.longitude},\
                   {vehicle.vehicle.position.bearing}, {vehicle.vehicle.position.odometer}, {vehicle.vehicle.position.speed}, {vehicle.vehicle.timestamp}, {vehicle.vehicle.congestion_level})')
                     
        cnxn.commit()
    # cursor.execute("COMMIT TRANSACTION;")
    cursor.close()
    cnxn.close()

def main(mytimer: func.TimerRequest) -> None:
    upload_vehicle_positions_into_database(get_vehicles_position())
    # utc_timestamp = datetime.datetime.utcnow().replace(
    #     tzinfo=datetime.timezone.utc).isoformat()

    # if mytimer.past_due:
    #     logging.info('The timer is past due!')

    f = "hdb"

    # feed = gtfs_realtime_pb2.FeedMessage()
    # response = requests.get('http://track.ua-gis.com/gtfs/lviv/vehicle_position')
    # feed.ParseFromString(response.content)
    # f = feed.entity

    # insert_data_from_url_to_sql_database()

    logging.info('Python timer trigger function ran at %s', f[0])
    # print(f[0].id)

main(111)



# def insert_data_from_url_to_sql_database():
#     # Retrieve data from URL

#     # Connect to SQL database
#     # cnxn = pyodbc.connect(f"Server=tcp:lvivtransportserver.database.windows.net,1433;Initial Catalog=lvivtransportdb;Persist Security Info=False;User ID=codelvivtransport;Password=C0delvivtransport;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;")
#     # cursor = cnxn.cursor()
#     # Insert data into SQL database
#     for marshrutka in f:
#         logging.info('hello %s', marshrutka.vehicle.vehicle.id)
#     #     cursor.execute(f'INSERT INTO vehicle_data (id,trip_id,route_id,schedule_relationship,vehicle_id,license_plate,latitude,longitude,bearing,odometer,speed,timestamp,congestion_level) VALUES ({marshrutka.id}, {marshrutka.vehicle.trip.trip_id}, {marshrutka.vehicle.trip.route_id}, {marshrutka.vehicle.trip.schedule_relationship},\
#     #                {marshrutka.vehicle.vehicle.id}, {marshrutka.vehicle.vehicle.license_plate}, {marshrutka.vehicle.position.latitude}, {marshrutka.vehicle.position.longitude},\
#     #                {marshrutka.vehicle.position.bearing}, {marshrutka.vehicle.position.odometer}, {marshrutka.vehicle.position.speed}, {marshrutka.vehicle.timestamp}, {marshrutka.vehicle.congestion_level})')
                     
#     #     cnxn.commit()
#     # cursor.close()
#     # Close the connection
#     # cnxn.close()