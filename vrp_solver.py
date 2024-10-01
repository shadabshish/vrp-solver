import math
import sys
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
def load_vrp_data(file_contents):
    loads = []
    lines = file_contents.splitlines()[1:]  # Skip header
    for line in lines:
        parts = line.split()
        load_id = int(parts[0])
        pickup = Point(*map(float, parts[1].strip("()").split(",")))
        dropoff = Point(*map(float, parts[2].strip("()").split(",")))
        loads.append(Load(load_id, pickup, dropoff))
    return loads

# Assign load to the drivers ensuring that no driver exceeds the 720-minute shift limit
def assign_loads_to_drivers_strict(loads):
    depot = Point(0, 0)
    drivers = defaultdict(list)
    driver_id = 1
    max_minutes = 720  # 12 hours limit
    remaining_loads = loads[:]
    total_driven_minutes = 0

    while remaining_loads:
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

            # Calculate potential new total if this load is added
            potential_total = total_minutes + to_pickup + to_dropoff + to_depot

            # Check if adding this load exceeds the driver's time limit (STRICT)
            if potential_total <= max_minutes:
                current_driver.append(closest_load.load_id)
                total_minutes += to_pickup + to_dropoff
                total_driven_minutes += to_pickup + to_dropoff
                current_location = closest_load.dropoff
                remaining_loads.remove(closest_load)
            else:
                break

        # After assigning loads to the current driver, add the return to depot
        if current_driver:
            drivers[driver_id] = current_driver
            driver_id += 1

        # If the current driver cannot take more loads, a new driver will start
        if not current_driver and remaining_loads:
            current_driver = []

    return drivers, total_driven_minutes

# Helper function to get load by id
def get_load_by_id(load_id, loads):
    for load in loads:
        if load.load_id == load_id:
            return load
    return None

# Output solution with only the load assignments
def output_solution(drivers):
    for driver, load_ids in drivers.items():
        print(f"[{','.join(map(str, load_ids))}]")

# Solve the problem using the strict driver limits and output the load assignments
def solve_problem_strict(file_contents):
    loads = load_vrp_data(file_contents)
    drivers, _ = assign_loads_to_drivers_strict(loads)
    output_solution(drivers)

# Main function to handle command-line argument and solve the problem
def main():
    if len(sys.argv) != 2:
        print("Usage: python test.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            solve_problem_strict(file_contents)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
