from datetime import datetime, timedelta

class DeliveryTruck:
    def __init__(self, max_capacity, avg_speed, initial_load, delivery_list, total_distance, current_location, start_time):
        self.max_capacity = max_capacity
        self.avg_speed = avg_speed
        self.current_load = initial_load
        self.delivery_list = delivery_list
        self.total_distance = total_distance
        self.current_location = current_location
        self.start_time = start_time
        self.current_time = start_time

    def __str__(self):
        return (f"Capacity: {self.max_capacity}, Speed: {self.avg_speed}, Load: {self.current_load}, "
                f"Packages: {self.delivery_list}, Mileage: {self.total_distance}, "
                f"Location: {self.current_location}, Departure Time: {self.start_time}")

    def add_package(self, package):
        if len(self.delivery_list) < self.max_capacity:
            self.delivery_list.append(package)

    def deliver_package(self, package, delivery_system):
        distance = delivery_system.get_distance(self.current_location, package.street_address)
        travel_time = distance / self.avg_speed
        self.total_distance += distance
        self.current_location = package.street_address
        self.current_time += timedelta(hours=travel_time)
        package.end_time = self.current_time
        package.start_time = self.current_time - timedelta(hours=travel_time)
        package.delivery_status = "Delivered"
        delivery_system.package_delivered(package)










