import logging
import requests
import time
from google.transit import gtfs_realtime_pb2
from google.cloud.sql.connector import Connector
import sqlalchemy


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
        self.db_conn.execute(sqlalchemy.text("""CREATE TABLE IF NOT EXISTS vehicle_data (
            id VARCHAR(255) NOT NULL,
            trip_id VARCHAR(255),
            route_id VARCHAR(255),
            vehicle_id VARCHAR(255),
            license_plate VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT,
            bearing FLOAT,
            speed FLOAT,
            timestamp INT)"""));
        self.db_conn.commit()
    
    def _fetch_vehicles(self):
        logging.info('Fetching vehicles')

        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get('http://track.ua-gis.com/gtfs/lviv/vehicle_position')
        feed.ParseFromString(response.content)
        return feed.entity
    
    def _upload_vehicles_into_database(self, vehicles):
        logging.info('Starting upload for %d vehicles', len(vehicles))

        insert_stmt = sqlalchemy.text(
            """INSERT INTO vehicle_data (id, trip_id, route_id,
                             vehicle_id, license_plate, latitude, longitude,
                             bearing, speed, timestamp) VALUES
                            (:id, :trip_id, :route_id,
                             :vehicle_id, :license_plate, :latitude, :longitude,
                             :bearing, :speed, :timestamp)""",
        )

        for vehicle in vehicles:
            id = vehicle.id
            vehicle = vehicle.vehicle
            self.db_conn.execute(insert_stmt, parameters={
                "id": id,
                "trip_id": vehicle.trip.trip_id,
                "route_id": vehicle.trip.route_id,
                "vehicle_id": vehicle.vehicle.id,
                "license_plate": vehicle.vehicle.license_plate,
                "latitude": vehicle.position.latitude,
                "longitude": vehicle.position.longitude,
                "bearing": vehicle.position.bearing,
                "speed": vehicle.position.speed,
                "timestamp": vehicle.timestamp
            })

        self.db_conn.commit()
        
    def run(self):
        n=0
        while n<=200:
            start = time.time()
            self._upload_vehicles_into_database(self._fetch_vehicles())
            diff = start - time.time()
            print(diff)
            n+=1
            if 10 - diff > 0:
                sleep = 10 - diff
            else:
                sleep = 0
            time.sleep(sleep)


def main() -> None:
    transport_service = TransportService()
    transport_service.run()


if __name__ == "__main__":
    main()
