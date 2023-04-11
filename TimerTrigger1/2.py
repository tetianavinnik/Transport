from google.protobuf.json_format import MessageToDict
import time
import sys
from google.transit import gtfs_realtime_pb2
import requests
import math
from math import atan, atan2, radians, cos, sin, sqrt
import logging
from google.cloud.sql.connector import Connector
import sqlalchemy
import datetime


class TransportService:
    def __init__(self) -> None:
        conn = Connector().connect(
           "peaceful-impact-382015:us-central1:lvivtransport",
           "pymysql",
           user="lvivtransport",
           password="root",
           db="lvivtransportdb"
        )
        pool = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=lambda: conn
        )
        self.db_conn = pool.connect()
        self._create_table()
    
    def _create_table(self):
        self.db_conn.execute(sqlalchemy.text("""CREATE TABLE IF NOT EXISTS on_stop_data (
            id VARCHAR(255) NOT NULL,
            trip_id VARCHAR(255),
            route_id VARCHAR(255),
            vehicle_id VARCHAR(255),
            license_plate VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT,
            bearing FLOAT,
            speed FLOAT,
            timestamp INT,
            stop_id INT,
            stop_code VARCHAR(255),
            stop_name VARCHAR(255),
            stop_desc VARCHAR(255),
            stop_lat FLOAT,
            stop_lon FLOAT,
            bearing1 INT,
            bearing2 INT)"""));
        self.db_conn.commit()
    
    def _upload_vehicles_into_database(self, vehicles):
        insert_stmt = sqlalchemy.text(
            """INSERT INTO on_stop_data (id, trip_id, route_id,
                             vehicle_id, license_plate, latitude, longitude,
                             bearing, speed, timestamp, stop_id, stop_code,
                             stop_name, stop_desc, stop_lat, stop_lon,
                             bearing1, bearing2) VALUES
                            (:id, :trip_id, :route_id,
                             :vehicle_id, :license_plate, :latitude, :longitude,
                             :bearing, :speed, :timestamp, :stop_id, :stop_code,
                             :stop_name, :stop_desc, :stop_lat, :stop_lon, :bearing1,
                             :bearing2)""",
        )

        self._analyze(insert_stmt)
        self.db_conn.commit()

    def _haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # radius of Earth in meters
        phi1 = radians(lat1)
        phi2 = radians(lat2)
        delta_phi = radians(lat2 - lat1)
        delta_lambda = radians(lon2 - lon1)
        a = sin(delta_phi/2)**2 + cos(phi1)*cos(phi2)*sin(delta_lambda/2)**2
        c = 2*atan2(sqrt(a), sqrt(1 - a))
        distance = R*c
        return distance
    
    def _analyze(self, insert_stmt):
        today = datetime.datetime.now().date()

        query = sqlalchemy.text("""
            SELECT id, trip_id, route_id, vehicle_id, license_plate, latitude, longitude, bearing, speed, timestamp
            FROM vehicle_data
            WHERE DATE(FROM_UNIXTIME(timestamp)) = :today
        """)
        result = self.db_conn.execute(query, today=today)
        
        with open(f"/home/tetiana/Transport/stops.txt", "r") as f:
            stop_lst = []
            for stop in f:
                stop_lst.append(stop)

            for row in result:
                id, trip_id, route_id, vehicle_id, license_plate, latitude, longitude, bearing, speed, timestamp = row
                for stop in stop_lst:
                    stop = stop.strip().split(',')
                    stop_id = int(stop[0])
                    stop_code = stop[1]
                    stop_name = stop[2]
                    stop_desc = stop[3]
                    stop_lat = float(stop[-4])
                    stop_lon = float(stop[-3])
                    stop_b1 = float(stop[-2])
                    stop_b2 = float(stop[-1])
                    distance = self._haversine(stop_lat, stop_lon, latitude, longitude)
                    if distance <= 100:
                        check = False
                        if stop_b1 > stop_b2:
                            if (bearing >= stop_b1 and bearing <= 360) or (bearing >= 0 and bearing <= stop_b2):
                                check = True
                        else:
                            if bearing >= stop_b1 and bearing <= stop_b2:
                                check = True
                        if check:
                            self.db_conn.execute(insert_stmt, parameters={
                                "id": id,
                                "trip_id": trip_id,
                                "route_id": route_id,
                                "vehicle_id": vehicle_id,
                                "license_plate": license_plate,
                                "latitude": latitude,
                                "longitude": longitude,
                                "bearing": bearing,
                                "speed": speed,
                                "timestamp": timestamp,
                                "stop_id": stop_id,
                                "stop_code": stop_code,
                                "stop_name": stop_name,
                                "stop_desc": stop_desc,
                                "stop_lat": stop_lat,
                                "stop_lon": stop_lon
                            })
        
    def run(self):
        self._upload_vehicles_into_database()


def main() -> None:
    transport_service = TransportService()
    transport_service.run()


if __name__ == "__main__":
    main()


