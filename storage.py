import os
import csv
from datetime import datetime
from models import (
    Admin, Customer, Car, Showroom, Garage, Service,
    BuyRentProcess, ServiceProcess, Reservation
)

#files
DATA_DIR = "data"

FILES = {
    "cars": os.path.join(DATA_DIR, "cars.csv"),
    "customers": os.path.join(DATA_DIR, "customers.csv"),
    "showrooms": os.path.join(DATA_DIR, "showrooms.csv"),
    "garages": os.path.join(DATA_DIR, "garages.csv"),
    "services": os.path.join(DATA_DIR, "services.csv"),
    "buy_rent_process": os.path.join(DATA_DIR, "buy_rent_process.csv"),
    "service_process": os.path.join(DATA_DIR, "service_process.csv"),
    "reservations": os.path.join(DATA_DIR, "reservations.csv"),
    "service_request_queue": os.path.join(DATA_DIR, "service_request_queue.csv"),
    "admin_action_stack": os.path.join(DATA_DIR, "admin_action_stack.csv"),
}

#DS
cars_by_id = {}
customers_by_id = {}
showrooms_by_id = {}
garages_by_id = {}
services_by_id = {}
reservations_by_id = {}

buy_rent_history = []
service_history = []

#queue (FIFO) for service requests
service_request_queue = []

#stack (LIFO) for admin actions (undo functionality)
admin_action_stack = []

def ensure_data_directory():
    """Create the data directory if it doesn't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def ensure_file_exists(filepath, header):
    """Create a CSV file with header if it doesn't exist."""
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header + '\n')


#load functions
def load_cars():
    """Load all cars from cars.csv into memory."""
    global cars_by_id
    cars_by_id = {}
    
    filepath = FILES["cars"]
    ensure_file_exists(filepath, "id,make,model,year,price,installment,showroom_id,available")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            

        for line in lines[1:]:
            line = line.strip()

            if not line:  
                continue
            
            try:
                car = Car.from_csv_row(line)
                cars_by_id[car.id] = car
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid car row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty cars.")
    
    return cars_by_id


def load_customers():
    """Load all customers from customers.csv into memory."""
    global customers_by_id
    customers_by_id = {}
    
    filepath = FILES["customers"]
    ensure_file_exists(filepath, "id,username,password,phone")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines[1:]: #skip headfer
            line = line.strip()
            if not line:
                continue
            
            try:
                customer = Customer.from_csv_row(line)
                customers_by_id[customer.id] = customer
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid customer row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty customers.")
    
    return customers_by_id

def load_showrooms():
    """Load all showrooms from showrooms.csv into memory."""
    global showrooms_by_id
    showrooms_by_id = {}
    
    filepath = FILES["showrooms"]
    ensure_file_exists(filepath, "id,name,location,phone,car_ids")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        #skiping header
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            try:
                showroom = Showroom.from_csv_row(line)
                showrooms_by_id[showroom.id] = showroom
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid showroom row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty showrooms.")
    
    return showrooms_by_id


def load_garages():
    """Load all garages from garages.csv into memory."""
    global garages_by_id
    garages_by_id = {}
    
    filepath = FILES["garages"]
    ensure_file_exists(filepath, "id,name,location,phone,service_ids")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        #skipping header
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            try:
                garage = Garage.from_csv_row(line)
                garages_by_id[garage.id] = garage
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid garage row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty garages.")
    
    return garages_by_id


def load_services():
    """Load all services from services.csv into memory."""
    global services_by_id
    services_by_id = {}
    
    filepath = FILES["services"]
    ensure_file_exists(filepath, "id,name,price")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        #skipping header
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            try:
                service = Service.from_csv_row(line)
                services_by_id[service.id] = service
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid service row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty services.")
    
    return services_by_id


def load_buy_rent_processes():
    """Load all buy/rent processes from buy_rent_process.csv into memory."""
    global buy_rent_history
    buy_rent_history = []
    
    filepath = FILES["buy_rent_process"]
    ensure_file_exists(filepath, "process_id,customer_id,date,amount,car_id,type")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Skip header
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            try:
                process = BuyRentProcess.from_csv_row(line)
                buy_rent_history.append(process)
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid buy/rent process row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty buy/rent history.")
    
    return buy_rent_history


def load_service_processes():
    """Load all service processes from service_process.csv into memory."""
    global service_history
    service_history = []
    
    filepath = FILES["service_process"]
    ensure_file_exists(filepath, "process_id,customer_id,date,amount,service_id,garage_id")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Skip header
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            try:
                process = ServiceProcess.from_csv_row(line)
                service_history.append(process)
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid service process row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty service history.")
    
    return service_history


def load_reservations():
    """Load all reservations from reservations.csv into memory."""
    global reservations_by_id
    reservations_by_id = {}
    
    filepath = FILES["reservations"]
    ensure_file_exists(filepath, "reservation_id,customer_id,car_id,start_time,expiry_time")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Skip header
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            try:
                reservation = Reservation.from_csv_row(line)
                reservations_by_id[reservation.reservation_id] = reservation
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid reservation row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty reservations.")
    
    return reservations_by_id


def load_service_request_queue():
    """Load service request queue from service_request_queue.csv into memory."""
    global service_request_queue
    service_request_queue = []
    
    filepath = FILES["service_request_queue"]
    ensure_file_exists(filepath, "request_id,customer_id,service_id,garage_id,timestamp,status")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        #skip header
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            try:
                parts = line.split(',')
                request = {
                    'request_id': int(parts[0]),
                    'customer_id': int(parts[1]),
                    'service_id': int(parts[2]),
                    'garage_id': int(parts[3]),
                    'timestamp': parts[4],
                    'status': parts[5]
                }
                service_request_queue.append(request)
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid service request row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty service request queue.")
    
    return service_request_queue


def load_admin_action_stack():
    """Load admin action stack from admin_action_stack.csv into memory."""
    global admin_action_stack
    admin_action_stack = []
    
    filepath = FILES["admin_action_stack"]
    ensure_file_exists(filepath, "action_id,admin_id,action_type,entity_type,entity_id,timestamp,details")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        #skip header
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            try:
                parts = line.split(',')
                action = {
                    'action_id': int(parts[0]),
                    'admin_id': int(parts[1]),
                    'action_type': parts[2],
                    'entity_type': parts[3],
                    'entity_id': int(parts[4]),
                    'timestamp': parts[5],
                    'details': parts[6] if len(parts) > 6 else ''
                }
                admin_action_stack.append(action)
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid admin action row: {line} - Error: {e}")
                
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty admin action stack.")
    
    return admin_action_stack


def load_all_data():
    """Load all data from CSV files into memory. This function should be called once when the program starts."""
    ensure_data_directory()
    
    print("Loading all data...")
    
    load_cars()
    load_customers()
    load_showrooms()
    load_garages()
    load_services()
    load_buy_rent_processes()
    load_service_processes()
    load_reservations()
    load_service_request_queue()
    load_admin_action_stack()
    
    print(f"Loaded: {len(cars_by_id)} cars, {len(customers_by_id)} customers, "
          f"{len(showrooms_by_id)} showrooms, {len(garages_by_id)} garages, "
          f"{len(services_by_id)} services, {len(buy_rent_history)} buy/rent processes, "
          f"{len(service_history)} service processes, {len(reservations_by_id)} reservations, "
          f"{len(service_request_queue)} service requests, {len(admin_action_stack)} admin actions")
    
    return {
        "cars": cars_by_id,
        "customers": customers_by_id,
        "showrooms": showrooms_by_id,
        "garages": garages_by_id,
        "services": services_by_id,
        "buy_rent_history": buy_rent_history,
        "service_history": service_history,
        "reservations": reservations_by_id,
        "service_request_queue": service_request_queue,
        "admin_action_stack": admin_action_stack
    }


#save functions
def save_cars():
    """Save all cars from memory to cars.csv."""
    filepath = FILES["cars"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("id,make,model,year,price,installment,showroom_id,available\n")
        
        # Write data
        for car in cars_by_id.values():
            f.write(car.to_csv_row() + '\n')


def save_customers():
    """Save all customers from memory to customers.csv."""
    filepath = FILES["customers"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("id,username,password,phone\n")
        
        # Write data
        for customer in customers_by_id.values():
            f.write(customer.to_csv_row() + '\n')


def save_showrooms():
    """Save all showrooms from memory to showrooms.csv."""
    filepath = FILES["showrooms"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("id,name,location,phone,car_ids\n")
        
        # Write data
        for showroom in showrooms_by_id.values():
            f.write(showroom.to_csv_row() + '\n')


def save_garages():
    """Save all garages from memory to garages.csv."""
    filepath = FILES["garages"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("id,name,location,phone,service_ids\n")
        
        # Write data
        for garage in garages_by_id.values():
            f.write(garage.to_csv_row() + '\n')


def save_services():
    """Save all services from memory to services.csv."""
    filepath = FILES["services"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("id,name,price\n")
        
        # Write data
        for service in services_by_id.values():
            f.write(service.to_csv_row() + '\n')


def save_buy_rent_processes():
    """Save all buy/rent processes from memory to buy_rent_process.csv."""
    filepath = FILES["buy_rent_process"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("process_id,customer_id,date,amount,car_id,type\n")
        
        # Write data
        for process in buy_rent_history:
            f.write(process.to_csv_row() + '\n')


def save_service_processes():
    """Save all service processes from memory to service_process.csv."""
    filepath = FILES["service_process"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("process_id,customer_id,date,amount,service_id,garage_id\n")
        
        # Write data
        for process in service_history:
            f.write(process.to_csv_row() + '\n')


def save_reservations():
    """Save all reservations from memory to reservations.csv."""
    filepath = FILES["reservations"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("reservation_id,customer_id,car_id,start_time,expiry_time\n")
        
        # Write data
        for reservation in reservations_by_id.values():
            f.write(reservation.to_csv_row() + '\n')


def save_service_request_queue():
    """Save service request queue from memory to service_request_queue.csv."""
    filepath = FILES["service_request_queue"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        #write header
        f.write("request_id,customer_id,service_id,garage_id,timestamp,status\n")
        
        #write data
        for request in service_request_queue:
            f.write(f"{request['request_id']},{request['customer_id']},{request['service_id']},"
                   f"{request['garage_id']},{request['timestamp']},{request['status']}\n")


def save_admin_action_stack():
    """Save admin action stack from memory to admin_action_stack.csv."""
    filepath = FILES["admin_action_stack"]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        #write header
        f.write("action_id,admin_id,action_type,entity_type,entity_id,timestamp,details\n")
        
        #write data
        for action in admin_action_stack:
            details = action.get('details', '')
            f.write(f"{action['action_id']},{action['admin_id']},{action['action_type']},"
                   f"{action['entity_type']},{action['entity_id']},{action['timestamp']},{details}\n")


def save_all_data():
    """Save all in-memory data structures back to CSV files.Called before program exit."""
    print("Saving all data...")
    
    save_cars()
    save_customers()
    save_showrooms()
    save_garages()
    save_services()
    save_buy_rent_processes()
    save_service_processes()
    save_reservations()
    save_service_request_queue()
    save_admin_action_stack()
    
    print("All data saved successfully")


#id management
def next_id_for(entity_type):
    """Generate the next unique ID for a given entity type."""
    entity_type = entity_type.lower()
    
    if entity_type == "car":
        if not cars_by_id:
            return 1
        return max(cars_by_id.keys()) + 1
    
    elif entity_type == "customer":
        if not customers_by_id:
            return 1
        return max(customers_by_id.keys()) + 1
    
    elif entity_type == "showroom":
        if not showrooms_by_id:
            return 1
        return max(showrooms_by_id.keys()) + 1
    
    elif entity_type == "garage":
        if not garages_by_id:
            return 1
        return max(garages_by_id.keys()) + 1
    
    elif entity_type == "service":
        if not services_by_id:
            return 1
        return max(services_by_id.keys()) + 1
    
    elif entity_type == "buy_rent_process":
        if not buy_rent_history:
            return 1
        return max(p.process_id for p in buy_rent_history) + 1
    
    elif entity_type == "service_process":
        if not service_history:
            return 1
        return max(p.process_id for p in service_history) + 1
    
    elif entity_type == "reservation":
        if not reservations_by_id:
            return 1
        return max(reservations_by_id.keys()) + 1
    
    else:
        raise ValueError(f"Unknown entity type: {entity_type}")


#reservation helpers
def clean_expired_reservations():
    """Remove expired reservations and make their cars available again. This function should be called periodically or when checking reservations."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expired_ids = []
    
    # Find expired reservations
    for res_id, reservation in reservations_by_id.items():
        if reservation.is_expired(current_time):
            expired_ids.append(res_id)
            
            # Mark the car as available again
            car_id = reservation.car_id
            if car_id in cars_by_id:
                cars_by_id[car_id].mark_available()
    
    # Remove expired reservations
    for res_id in expired_ids:
        del reservations_by_id[res_id]
    
    if expired_ids:
        print(f"Cleaned {len(expired_ids)} expired reservation(s)")
        save_reservations()
        save_cars()
    
    return len(expired_ids)


#access helpers
def get_car_by_id(car_id):
    """Retrieve a car by its ID."""
    return cars_by_id.get(int(car_id))


def get_customer_by_id(customer_id):
    """Retrieve a customer by their ID."""
    return customers_by_id.get(int(customer_id))


def get_showroom_by_id(showroom_id):
    """Retrieve a showroom by its ID."""
    return showrooms_by_id.get(int(showroom_id))


def get_garage_by_id(garage_id):
    """Retrieve a garage by its ID."""
    return garages_by_id.get(int(garage_id))


def get_service_by_id(service_id):
    """Retrieve a service by its ID."""
    return services_by_id.get(int(service_id))


def get_reservation_by_id(reservation_id):
    """Retrieve a reservation by its ID."""
    return reservations_by_id.get(int(reservation_id))


def get_all_cars():
    """Return a list of all cars."""
    return list(cars_by_id.values())


def get_all_customers():
    """Return a list of all customers."""
    return list(customers_by_id.values())


def get_all_showrooms():
    """Return a list of all showrooms."""
    return list(showrooms_by_id.values())


def get_all_garages():
    """Return a list of all garages."""
    return list(garages_by_id.values())


def get_all_services():
    """Return a list of all services."""
    return list(services_by_id.values())


def get_all_reservations():
    """Return a list of all reservations."""
    return list(reservations_by_id.values())


def get_all_buy_rent_processes():
    """Return a list of all buy/rent processes."""
    return list(buy_rent_history)


def get_all_service_processes():
    """Return a list of all service processes."""
    return list(service_history)

#crud helpers for cars
def add_car(car_object):
    """Add a new car to the system."""
    if car_object.id in cars_by_id:
        return False
    
    cars_by_id[car_object.id] = car_object
    save_cars()
    return True


def update_car(car_id, **fields):
    """Update an existing car's details."""
    car = get_car_by_id(car_id)
    if not car:
        return False
    
    car.update_details(**fields)
    save_cars()
    return True


def delete_car(car_id):
    """Delete a car from the system."""
    car_id = int(car_id)
    if car_id not in cars_by_id:
        return False
    
    # Remove car from showroom if it exists
    car = cars_by_id[car_id]
    showroom = get_showroom_by_id(car.showroom_id)
    if showroom:
        showroom.remove_car(car_id)
        save_showrooms()
    
    del cars_by_id[car_id]
    save_cars()
    return True

#crud helpers for customers
def add_customer(customer_object):
    """Add a new customer to the system."""
    if customer_object.id in customers_by_id:
        return False
    
    customers_by_id[customer_object.id] = customer_object
    save_customers()
    return True


def update_customer(customer_id, **fields):
    """Update an existing customer's details."""
    customer = get_customer_by_id(customer_id)
    if not customer:
        return False
    
    if 'username' in fields:
        customer.username = fields['username']
    if 'password' in fields:
        customer.password = fields['password']
    if 'phone' in fields:
        customer.phone = int(fields['phone'])
    
    save_customers()
    return True


def delete_customer(customer_id):
    """Delete a customer from the system."""
    customer_id = int(customer_id)
    if customer_id not in customers_by_id:
        return False
    
    del customers_by_id[customer_id]
    save_customers()
    return True


#crud helpers for showrooms
def add_showroom(showroom_object):
    """Add a new showroom to the system."""
    if showroom_object.id in showrooms_by_id:
        return False
    
    showrooms_by_id[showroom_object.id] = showroom_object
    save_showrooms()
    return True


def update_showroom(showroom_id, **fields):
    """Update an existing showroom's details."""
    showroom = get_showroom_by_id(showroom_id)
    if not showroom:
        return False
    
    showroom.update_details(**fields)
    save_showrooms()
    return True


def delete_showroom(showroom_id):
    """Delete a showroom from the system."""
    showroom_id = int(showroom_id)
    if showroom_id not in showrooms_by_id:
        return False
    
    del showrooms_by_id[showroom_id]
    save_showrooms()
    return True


#crud helpers for garages
def add_garage(garage_object):
    """Add a new garage to the system."""
    if garage_object.id in garages_by_id:
        return False
    
    garages_by_id[garage_object.id] = garage_object
    save_garages()
    return True


def update_garage(garage_id, **fields):
    """Update an existing garage's details."""
    garage = get_garage_by_id(garage_id)
    if not garage:
        return False
    
    garage.update_details(**fields)
    save_garages()
    return True


def delete_garage(garage_id):
    """Delete a garage from the system."""
    garage_id = int(garage_id)
    if garage_id not in garages_by_id:
        return False
    
    del garages_by_id[garage_id]
    save_garages()
    return True


#crud helpers for services
def add_service(service_object):
    """Add a new service to the system."""
    if service_object.id in services_by_id:
        return False
    
    services_by_id[service_object.id] = service_object
    save_services()
    return True


def update_service(service_id, **fields):
    """Update an existing service's details."""
    service = get_service_by_id(service_id)
    if not service:
        return False
    
    service.update_details(**fields)
    save_services()
    return True


def delete_service(service_id):
    """Delete a service from the system."""
    service_id = int(service_id)
    if service_id not in services_by_id:
        return False
    
    del services_by_id[service_id]
    save_services()
    return True


#crud helpers for reservations
def add_reservation(reservation_object):
    """Add a new reservation to the system."""
    if reservation_object.reservation_id in reservations_by_id:
        return False
    
    reservations_by_id[reservation_object.reservation_id] = reservation_object
    save_reservations()
    return True


def delete_reservation(reservation_id):
    """Delete a reservation from the system."""
    reservation_id = int(reservation_id)
    if reservation_id not in reservations_by_id:
        return False
    
    # Make the car available again
    reservation = reservations_by_id[reservation_id]
    car = get_car_by_id(reservation.car_id)
    if car:
        car.mark_available()
        save_cars()
    
    del reservations_by_id[reservation_id]
    save_reservations()
    return True


#helpers for processes (history)
def add_buy_rent_process(process_object):
    """Add a new buy/rent process to history."""
    buy_rent_history.append(process_object)
    save_buy_rent_processes()
    return True


def add_service_process(process_object):
    """Add a new service process to history."""
    service_history.append(process_object)
    save_service_processes()
    return True


#search and filter functions
def search_cars(filters=None):
    """Search for cars matching the given filters."""
    if not filters:
        return get_all_cars()
    
    results = []
    for car in cars_by_id.values():
        if car.matches_filter(filters):
            results.append(car)
    
    return results


def get_customer_by_username(username):
    """Find a customer by username."""
    for customer in customers_by_id.values():
        if customer.username.lower() == username.lower():
            return customer
    return None


def get_cars_in_showroom(showroom_id):
    """Get all cars in a specific showroom."""
    showroom = get_showroom_by_id(showroom_id)
    if not showroom:
        return []
    
    cars = []
    for car_id in showroom.car_ids:
        car = get_car_by_id(car_id)
        if car:
            cars.append(car)
    
    return cars


def get_services_in_garage(garage_id):
    """Get all services in a specific garage."""
    garage = get_garage_by_id(garage_id)
    if not garage:
        return []
    
    services = []
    for service_id in garage.service_ids:
        service = get_service_by_id(service_id)
        if service:
            services.append(service)
    
    return services


def get_customer_reservations(customer_id):
    """Get all reservations for a specific customer."""
    reservations = []
    for reservation in reservations_by_id.values():
        if reservation.customer_id == int(customer_id):
            reservations.append(reservation)
    
    return reservations


def get_customer_buy_rent_history(customer_id):
    """Get all buy/rent processes for a specific customer."""
    processes = []
    for process in buy_rent_history:
        if process.customer_id == int(customer_id):
            processes.append(process)
    
    return processes


def get_customer_service_history(customer_id):
    """Get all service processes for a specific customer."""
    processes = []
    for process in service_history:
        if process.customer_id == int(customer_id):
            processes.append(process)
    
    return processes


#queue operations (FIFO - first in first out)
def enqueue_service_request(customer_id, service_id, garage_id):
    """Add a service request to the end of the queue (enqueue operation)."""
    request_id = len(service_request_queue) + 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    request = {
        'request_id': request_id,
        'customer_id': customer_id,
        'service_id': service_id,
        'garage_id': garage_id,
        'timestamp': timestamp,
        'status': 'pending'
    }
    
    service_request_queue.append(request)
    save_service_request_queue()
    
    print(f"Service request #{request_id} added to queue at position {len(service_request_queue)}")
    return request_id


def dequeue_service_request():
    """Remove and return the first service request from the queue (dequeue operation)."""
    if not service_request_queue:
        print("Queue is empty. No service requests to process.")
        return None
    
    request = service_request_queue.pop(0)
    save_service_request_queue()
    
    print(f"Processing service request #{request['request_id']} from customer {request['customer_id']}")
    return request


def peek_service_request_queue():
    """View the first service request in the queue without removing it."""
    if not service_request_queue:
        return None
    return service_request_queue[0]


def get_queue_size():
    """Return the number of service requests in the queue."""
    return len(service_request_queue)


def view_service_request_queue():
    """Display all service requests in the queue."""
    if not service_request_queue:
        print("Service request queue is empty.")
        return []
    
    print(f"\nService Request Queue ({len(service_request_queue)} requests):")
    print("=" * 80)
    
    for i, request in enumerate(service_request_queue, 1):
        customer = get_customer_by_id(request['customer_id'])
        service = get_service_by_id(request['service_id'])
        garage = get_garage_by_id(request['garage_id'])
        
        customer_name = customer.username if customer else f"Customer #{request['customer_id']}"
        service_name = service.name if service else f"Service #{request['service_id']}"
        garage_name = garage.name if garage else f"Garage #{request['garage_id']}"
        
        print(f"Position {i}: Request #{request['request_id']}")
        print(f"  Customer: {customer_name}")
        print(f"  Service: {service_name}")
        print(f"  Garage: {garage_name}")
        print(f"  Timestamp: {request['timestamp']}")
        print(f"  Status: {request['status']}")
        print("-" * 80)
    
    return service_request_queue


#stack operations (LIFO - last in first out)
def push_admin_action(admin_id, action_type, entity_type, entity_id, details=""):
    """Push an admin action onto the stack (for undo functionality)."""
    action_id = len(admin_action_stack) + 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    action = {
        'action_id': action_id,
        'admin_id': admin_id,
        'action_type': action_type,
        'entity_type': entity_type,
        'entity_id': entity_id,
        'timestamp': timestamp,
        'details': details
    }
    
    admin_action_stack.append(action)
    save_admin_action_stack()
    
    print(f"Admin action #{action_id} ({action_type}) pushed to stack")
    return action_id


def pop_admin_action():
    """Pop the most recent admin action from the stack (for undo operation)."""
    if not admin_action_stack:
        print("Stack is empty. No actions to undo.")
        return None
    
    action = admin_action_stack.pop()
    save_admin_action_stack()
    
    print(f"Popped action #{action['action_id']}: {action['action_type']} on {action['entity_type']} #{action['entity_id']}")
    return action


def peek_admin_action_stack():
    """View the most recent admin action without removing it from the stack."""
    if not admin_action_stack:
        return None
    return admin_action_stack[-1]


def get_stack_size():
    """Return the number of admin actions in the stack."""
    return len(admin_action_stack)


def view_admin_action_stack(limit=10):
    """Display the most recent admin actions in the stack."""
    if not admin_action_stack:
        print("Admin action stack is empty.")
        return []
    
    display_count = min(limit, len(admin_action_stack))
    recent_actions = admin_action_stack[-display_count:]
    recent_actions.reverse()
    
    print(f"\nAdmin Action Stack (showing {display_count} most recent):")
    print("=" * 80)
    
    for action in recent_actions:
        print(f"Action #{action['action_id']}: {action['action_type'].upper()}")
        print(f"  Admin ID: {action['admin_id']}")
        print(f"  Entity: {action['entity_type']} #{action['entity_id']}")
        print(f"  Timestamp: {action['timestamp']}")
        if action.get('details'):
            print(f"  Details: {action['details']}")
        print("-" * 80)
    
    return recent_actions


def clear_admin_action_stack():
    """Clear all admin actions from the stack."""
    global admin_action_stack
    count = len(admin_action_stack)
    admin_action_stack = []
    save_admin_action_stack()
    print(f"Cleared {count} admin action(s) from stack")
    return count
