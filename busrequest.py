import requests
from google.transit import gtfs_realtime_pb2
import time
import csv
import displaytext

# Remember to replace the .zip (SURFACEGTFS) once a month. 
# TTC frequently updates stop IDs, adds buses, etc. 
TRIPS_URL = "https://bustime.ttc.ca/gtfsrt/trips"
VEHICLES_URL = "https://bustime.ttc.ca/gtfsrt/vehicles"
# replace this with the internal stop_id you found in stops.txt
TARGET_STOP_ID = "11242" 



def get_bus():
    stop_names = {}
    with open('SurfaceGTFS/stops.txt', mode='r') as f:
        for row in csv.DictReader(f):
            stop_names[row['stop_id']] = row['stop_name']

    trip_branches = {}
    with open('SurfaceGTFS/trips.txt', mode='r') as f:
        for row in csv.DictReader(f):
            trip_branches[row['trip_id']] = row['trip_headsign']


    v_response = requests.get(VEHICLES_URL)
    v_feed = gtfs_realtime_pb2.FeedMessage()
    v_feed.ParseFromString(v_response.content)
    
    # Map trip_id to vehicle info (Occupancy and ID)
    live_vehicles = {}
    for entity in v_feed.entity:
        if entity.HasField('vehicle'):
            t_id = entity.vehicle.trip.trip_id
            live_vehicles[t_id] = {
                "bus_no": entity.vehicle.vehicle.id,
                "crowd": entity.vehicle.occupancy_status 
            }


    t_response = requests.get(TRIPS_URL)
    t_feed = gtfs_realtime_pb2.FeedMessage()
    t_feed.ParseFromString(t_response.content)
    
    
    current_server_time = t_feed.header.timestamp
    
    predictions = []

    for entity in t_feed.entity:
        if entity.HasField('trip_update'):
            trip_id = entity.trip_update.trip.trip_id
            
            for update in entity.trip_update.stop_time_update:
                if update.stop_id == TARGET_STOP_ID:
                    # note: entity gtfs does everything in unix so have to change it into human-readable
                    arrival_time = update.arrival.time
                    delay_seconds = arrival_time - current_server_time
                    minutes_away = round(delay_seconds / 60)

                    if minutes_away >= 0:
                        
                        v_info = live_vehicles.get(trip_id, {"bus_no": "Unknown", "crowd": "N/A"})
                       
                        headsign = trip_branches.get(trip_id, "Route Unknown")
                        
                        if "Route Unknown" not in headsign: 

                            splitword = headsign.split()
                            hssplit = splitword[2:4]
                            shortened = " ".join(hssplit)

                            predictions.append({
                                "headsign": shortened,
                                "minutes": minutes_away,
                                "bus": v_info['bus_no'],
                                "crowd": v_info['crowd']
                            })

    predictions.sort(key=lambda x: x['minutes'])
    

    bus_strings = []



    print(f"\n--- Next 4 Buses for {stop_names.get(TARGET_STOP_ID, TARGET_STOP_ID)} ---")
    for p in predictions[:4]:

        line = f"{p['headsign']} | {p['minutes']} min"

        bus_strings.append(line)
        print(f"{p['headsign']} | {p['minutes']} min ")

    
    stop_title = stop_names.get(TARGET_STOP_ID, TARGET_STOP_ID)
    bus_strings.insert(0, f"-- {stop_title} --")
    displaytext.print_text(bus_strings, 5)


if __name__ == "__main__":
    get_bus()