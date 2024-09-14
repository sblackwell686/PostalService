import datetime

class DeliveryPackage:
    def __init__(self, package_id, street_address, city_name, state_code, postal_code, deadline, package_weight, delivery_status):
        self.package_id = package_id
        self.street_address = street_address
        self.city_name = city_name
        self.state_code = state_code
        self.postal_code = postal_code
        self.deadline = deadline
        self.package_weight = package_weight
        self.delivery_status = delivery_status
        self.start_time = None
        self.end_time = None
        self.truck_number = None  # New attribute for truck number

    def __str__(self):
        return (f"ID: {self.package_id}, Address: {self.street_address}, City: {self.city_name}, "
                f"State: {self.state_code}, Zip: {self.postal_code}, Deadline: {self.deadline}, "
                f"Weight: {self.package_weight}, Delivery Time: {self.end_time}, Status: {self.delivery_status}, "
                f"Delivered by Truck: {self.truck_number}")  # Include truck number

    def set_status(self, current_time):
        if self.end_time and self.end_time < current_time:
            self.delivery_status = "Delivered"
        elif self.start_time and self.start_time <= current_time:
            self.delivery_status = "En route"
        else:
            self.delivery_status = "At Hub"


