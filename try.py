
import json
from google.transit import gtfs_realtime_pb2
import requests
from google.protobuf.json_format import MessageToDict
import schedule
import time
import sys
import gtfs_kit as gk
from gtfslite.gtfs import GTFS
import csv
from google.protobuf.json_format import MessageToJson
from google.protobuf.descriptor import FieldDescriptor



n=0
def func():
    global n
    n+=1
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://track.ua-gis.com/gtfs/lviv/vehicle_position')
    feed.ParseFromString(response.content)
    repeated_container = feed.entity
    # s = str(f)
    # print(type(f))
    


    # Assuming repeated_container is your instance of RepeatedCompositeContainer

    # Decode the repeated_container into Python objects
    objects = []
    for message in repeated_container:
        object_dict = MessageToJson(message)
        objects.append(json.loads(object_dict))

    with open(r'C:\Users\TETYANA\Desktop\Транспорт\output.txt', 'r+') as f:

        if n == 1:
            objects = str(objects)[:-1] + ","
        elif n==2:
            objects = str(objects)[1:]
            f.write(objects)
            with open(r'C:\Users\TETYANA\Desktop\Транспорт\output.json', 'w+') as output_file:
                output_file.write("[")  # start of the JSON array

                # Loop over each line in the input file
                for i, line in enumerate(f):
                    # Remove any trailing newlines or whitespace
                   
                    line = line.strip()
                    print(line)
                    # Skip empty lines
                    if not line:
                        continue

                    # Parse the line as JSON
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing line {i}: {e}")
                        continue

                    # Write the parsed data to the output file
                    if i > 0:
                        output_file.write(",")
                    json.dump(data, output_file)

                output_file.write("]") 
            sys.exit()
        else:
            objects = str(objects)[1:-1] + ","
        f.write(objects)
    
    
    
        # objects = json.loads(objects)
        # json.dump(objects, f)
            # f.write('\n')


        # # Extract the field names and write them to the CSV file
        # field_names = []
        # for field_descriptor in message.DESCRIPTOR.fields:
        #     if field_descriptor.type == FieldDescriptor.TYPE_MESSAGE:
        #         for sub_field_descriptor in field_descriptor.message_type.fields:
        #             field_names.append(f'{field_descriptor.name}.{sub_field_descriptor.name}')
        #     else:
        #         field_names.append(field_descriptor.name)

        # with open(r'C:\Users\TETYANA\Desktop\Транспорт\output.csv', 'w', newline='') as csv_file:
        #     writer = csv.DictWriter(csv_file, fieldnames=field_names)
        #     writer.writeheader()

        #     # Extract the data and write it to the CSV file
        #     for obj in objects:
        #         flattened_obj = {}
        #         for key, value in obj.items():
        #             if isinstance(value, dict):
        #                 for sub_key, sub_value in value.items():
        #                     flattened_obj[f'{key}.{sub_key}'] = sub_value
        #             else:
        #                 flattened_obj[key] = value
        #         writer.writerow(flattened_obj)


    # with open(r'C:\Users\TETYANA\Desktop\Транспорт\result1', "a") as file:
    #     file.write(s)
    # with open(r'C:\Users\TETYANA\Desktop\Транспорт\transport_number', "a") as file:
    #     file.write(str(len(f))+"\n")

    # if n==2:
    #     with open(r'C:\Users\TETYANA\Desktop\Транспорт\output.json', 'r+') as f:
    #         data = json.load(f)
    #         json.dump(data, f)
    #     sys.exit()

#     # print('There are {} buses in the dataset.'.format(len(feed.entity)))
#     # # looking closely at the first bus
#     # bus = feed.entity[0]

#     # print(feed.entity)


#     # for entity in feed.entity:
#     #   if entity.HasField('trip_update'):
#     #     print(entity.trip_update)

# # func()

# # def func1():

schedule.every(2).seconds.do(func)

# # for _ in range(3):
# #     schedule.run_pending()
# #     time.sleep(1)

# # schedule.every().seconds.days.at("18:29").do(func)

while True:
    schedule.run_pending()
    time.sleep(0.083)


# gtfs = GTFS.load_zip('http://track.ua-gis.com/gtfs/lviv/static.zip')

# print(gtfs.summary())

# import requests

# url = r'http://track.ua-gis.com/gtfs/lviv/static.zip'
# output = r'C:\Users\TETYANA\Desktop\Транспорт\downloaded_file.zip'

# r = requests.get(url)
# with open(output, 'wb') as f:
#     f.write(r.content)


# import requests, zipfile, io

# url = 'http://track.ua-gis.com/gtfs/lviv/static.zip'
# filename = r'C:\Users\TETYANA\Desktop\Транспорт\shapes.txt'

# r = requests.get(url)
# z = zipfile.ZipFile(io.BytesIO(r.content))
# z.extractall()

# import pandas as pd
# df = pd.read_csv(filename, sep=',')
# print(df)