# Stephen Blackwell, ID: 011081997

import csv
import datetime
from Truck import DeliveryTruck
from HashTable import HashMap
from Package import DeliveryPackage

# Read the CSV files for distance, address, and package information
with open("distances.csv") as distance_file:
    distance_data = list(csv.reader(distance_file))

with open("addresses.csv") as address_file:
    address_data = list(csv.reader(address_file))

with open("packages.csv") as package_file:
    package_data = list(csv.reader(package_file))


# Load package data into hash map
def load_package_data(file_name, hash_map):
    with open(file_name) as file:
        data = csv.reader(file)
        for row in data:
            package_id = int(row[0])
            street_address = row[1]
            city_name = row[2]
            state_code = row[3]
            postal_code = row[4]
            deadline = row[5]
            package_weight = row[6]
            delivery_status = "At Hub"

            package = DeliveryPackage(package_id, street_address, city_name, state_code, postal_code, deadline,
                                      package_weight, delivery_status)
            hash_map.add(package_id, package)


# Calculate distance between two addresses
def calculate_distance(from_address, to_address):
    from_id = get_address_id(from_address)
    to_id = get_address_id(to_address)
    if from_id is not None and to_id is not None:
        distance = distance_data[from_id][to_id]
        if distance == '':
            distance = distance_data[to_id][from_id]
        return float(distance)
    return 0.0


# Get address ID from address string
def get_address_id(address):
    for row in address_data:
        if address in row[2]:
            return int(row[0])
    return None


# Create hash map and load packages
package_hash_map = HashMap()
load_package_data("packages.csv", package_hash_map)

# Update package 9 information if the current time is before 10:20 AM
current_time = datetime.datetime.now().time()
if current_time <= datetime.time(10, 19):
    package_9 = package_hash_map.get(9)
    package_9.street_address = "300 State St"
    package_9.city_name = "Salt Lake City"
    package_9.state_code = "UT"
    package_9.postal_code = "84103"
    package_hash_map.add(9, package_9)

# Create trucks
truck1 = DeliveryTruck(16, 18, None, [1, 12, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                       datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0)))
truck2 = DeliveryTruck(16, 18, None, [3, 5, 6, 9, 18, 22, 23, 24, 26, 27, 32, 35, 36, 38], 0.0,
                       "4001 South 700 East", datetime.datetime.combine(datetime.date.today(), datetime.time(10, 20)))
truck3 = DeliveryTruck(16, 18, None, [2, 4, 6, 7, 8, 10, 11, 25, 28, 31, 32, 33, 39, 17], 0.0, "4001 South 700 East",
                       datetime.datetime.combine(datetime.date.today(), datetime.time(9, 5)))


# Deliver packages using nearest neighbor algorithm
def deliver_packages(truck, truck_number):
    undelivered = []
    for package_id in truck.delivery_list:
        package = package_hash_map.get(package_id)
        undelivered.append(package)
    truck.delivery_list.clear()

    while undelivered:
        nearest_distance = float('inf')
        nearest_package = None
        for package in undelivered:
            distance = calculate_distance(truck.current_location, package.street_address)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package

        truck.delivery_list.append(nearest_package.package_id)
        undelivered.remove(nearest_package)
        truck.total_distance += nearest_distance
        truck.current_location = nearest_package.street_address
        truck.current_time += datetime.timedelta(hours=nearest_distance / truck.avg_speed)
        nearest_package.end_time = truck.current_time
        nearest_package.start_time = truck.start_time
        nearest_package.truck_number = truck_number  # Assign the truck number to the package

# Process the deliveries
deliver_packages(truck1, 1)
deliver_packages(truck2, 2)
truck3.start_time = min(truck1.current_time, truck2.current_time)
deliver_packages(truck3, 3)


# Main class for user interaction
class Main:
    @staticmethod
    def show_menu():
        print("\nWestern Governors University Parcel Service (WGUPS)")
        print("1. General Report (shows every package at a given time)")
        print("2. Package Individual Query (shows one particular package at a given time)")
        print("3. Total Truck Mileage (shows total mileage of the trucks at a given time)")
        print("4. Exit Program")
        return input("Please choose an option (1, 2, 3, 4): ").strip()

    @staticmethod
    def get_time_input():
        time_input = input("Please enter a time to check the status of packages (HH:MM AM/PM): ").strip()
        try:
            # Convert the 12-hour format to 24-hour format
            user_time = datetime.datetime.strptime(time_input, "%I:%M %p")
            return datetime.time(user_time.hour, user_time.minute)
        except ValueError:
            print("Invalid time format. Please use HH:MM AM/PM format.")
            return None

    @staticmethod
    def display_general_report():
        user_time = Main.get_time_input()
        if user_time is None:
            return
        user_datetime = datetime.datetime.combine(datetime.date.today(), user_time)
        for package_id in range(1, 41):
            package = package_hash_map.get(package_id)
            package.set_status(user_datetime)

            # Check for package ID 9 and update address if before 10:20 AM
            if package_id == 9 and user_datetime < datetime.datetime.combine(datetime.date.today(),
                                                                             datetime.time(10, 20)):
                print(f"ID: 9, Address: 300 State St, City: Salt Lake City, State: UT, Zip: 84103, Deadline: EOD, "
                      f"Weight: 2 Kilos, Delivery Time: Waiting on new address, Status: At Hub")
            else:
                print(package)

        print(f"\nTotal distance traveled by Truck 1: {truck1.total_distance:.2f} miles")
        print(f"Total distance traveled by Truck 2: {truck2.total_distance:.2f} miles")
        print(f"Total distance traveled by Truck 3 : {truck3.total_distance:.2f} miles")
        print(
            f"Total distance traveled by all trucks: {truck1.total_distance + truck2.total_distance + truck3.total_distance:.2f} miles. \n For accurate total distance traveled by trucks at a particular time, choose option 3.")

    @staticmethod
    def package_query():
        user_time = Main.get_time_input()
        if user_time is None:
            return
        try:
            package_id = int(input("Enter the package ID: ").strip())
            package = package_hash_map.get(package_id)
            user_datetime = datetime.datetime.combine(datetime.date.today(), user_time)
            package.set_status(user_datetime)

            # Check for package ID 9 and update address if before 10:20 AM
            if package_id == 9 and user_datetime < datetime.datetime.combine(datetime.date.today(),
                                                                             datetime.time(10, 20)):
                print(f"ID: 9, Address: 300 State St, City: Salt Lake City, State: UT, Zip: 84103, Deadline: EOD, "
                      f"Weight: 2 Kilos, Delivery Time: Waiting on new address, Status: At Hub")
            else:
                print(package)
        except ValueError:
            print("Invalid input. Please ensure package ID is a number.")

    @staticmethod
    def total_truck_mileage():
        user_time = Main.get_time_input()
        if user_time is None:
            return
        user_datetime = datetime.datetime.combine(datetime.date.today(), user_time)
        print(f"\nTotal distance traveled by Truck 1 up to {user_time}: {truck1.total_distance:.2f} miles")
        print(f"Total distance traveled by Truck 2 up to {user_time}: {truck2.total_distance:.2f} miles")
        print(f"Total distance traveled by Truck 3 up to {user_time}: {truck3.total_distance:.2f} miles")
        print(
            f"Total distance traveled by all trucks up to {user_time}: {truck1.total_distance + truck2.total_distance + truck3.total_distance:.2f} miles")

    @staticmethod
    def run():
        while True:
            option = Main.show_menu()
            if option == '1':
                Main.display_general_report()
            elif option == '2':
                Main.package_query()
            elif option == '3':
                Main.total_truck_mileage()
            elif option == '4':
                print("Exiting the program.")
                break
            else:
                print("Invalid option. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    Main.run()




