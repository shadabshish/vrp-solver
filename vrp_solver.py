import math
from collections import defaultdict
# Class definitions for Point and Load
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Load:
    def __init__(self, load_id, pickup, dropoff):
        self.load_id = load_id
        self.pickup = pickup
        self.dropoff = dropoff


# Function to calculate the distance
def euclidean_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# Load VRP data from files
def load_vrp_data(file_path):
    loads = []
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:] #this part is to skip header
        for line in lines:
            parts = line.split()
            load_id = int(parts[0])
            pickup = Point(*map(float, parts[1].scrip("()").split(",")))
            dropoff = Point(*map(float, parts[2].strip("()").split(",")))
            loads.append(Load(load_id, pickup, dropoff))
    return loads

# Assign load to the drivers
def assign_loads_to_drivers(loads):
    depot = Point(0, 0)
    drivers = defaultdict(list)
    driver_id = 1
    max_minutes = 720 # 12 hours limit
    remaining_loads = loads[:]
    total_driven_minutes = 0

    while   remaining_loads:
        current_driver = []
        total_minutes = 0
        current_location = depot
        while remaining_loads:
            # Find the closest load to the current location
            closest_load = min(
                remaining_loads,
                key=lambda load: euclidean_distance(current_location, load.pickup)
            )
            to_pickup = euclidean_distance(current_location, closest_load.pickup)
            to_dropoff = euclidean_distance(closest_load.pickup, closest_load.dropoff)
            to_depot = euclidean_distance(closest_load.dropoff, depot)

            # Check if adding this load exceeds the driver's time limit
            if total_minutes + to_pickup + to_dropoff + to_depot <= max_minutes:
                current_driver.append(closest_load.load_id)
                total_minutes += to_pickup + to_dropoff
                total_driven_minutes += to_pickup + to_dropoff + to_depot
                current_location = closest_load.dropoff
                remaining_loads.remove(closest_load)
            else:
                break

            # Assign the current driver their loads and start a new driver
        if current_driver:
            drivers[driver_id] = current_driver
            driver_id += 1

# Function to calculate cost
def calculate_cost(drivers, total_driven_minutes):
    number_of_drivers = len(drivers)
    total_cost = 500 * number_of_drivers + total_driven_minutes
    return total_cost

