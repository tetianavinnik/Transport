import pyodbc
import urllib.request
import json
from google.transit import gtfs_realtime_pb2
import requests
from google.protobuf.json_format import MessageToDict
import schedule
import time
import sys
import logging


def insert_data_from_url_to_sql_database():
    # Retrieve data from URL
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://track.ua-gis.com/gtfs/lviv/vehicle_position')
    feed.ParseFromString(response.content)
    f = feed.entity

    # Connect to SQL database
    # cnxn = pyodbc.connect(f"Server=tcp:lvivtransportserver.database.windows.net,1433;Initial Catalog=lvivtransportdb;Persist Security Info=False;User ID=codelvivtransport;Password=C0delvivtransport;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;")
    # cursor = cnxn.cursor()
    # Insert data into SQL database
    for marshrutka in f:
        logging.info('hello %s', marshrutka.vehicle.vehicle.id)
    #     cursor.execute(f'INSERT INTO vehicle_data (id,trip_id,route_id,schedule_relationship,vehicle_id,license_plate,latitude,longitude,bearing,odometer,speed,timestamp,congestion_level) VALUES ({marshrutka.id}, {marshrutka.vehicle.trip.trip_id}, {marshrutka.vehicle.trip.route_id}, {marshrutka.vehicle.trip.schedule_relationship},\
    #                {marshrutka.vehicle.vehicle.id}, {marshrutka.vehicle.vehicle.license_plate}, {marshrutka.vehicle.position.latitude}, {marshrutka.vehicle.position.longitude},\
    #                {marshrutka.vehicle.position.bearing}, {marshrutka.vehicle.position.odometer}, {marshrutka.vehicle.position.speed}, {marshrutka.vehicle.timestamp}, {marshrutka.vehicle.congestion_level})')
                     
    #     cnxn.commit()
    # cursor.close()
    # Close the connection
    # cnxn.close()