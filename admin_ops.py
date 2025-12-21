from datetime import datetime
from models import Admin, Car, Showroom, Garage, Service, ServiceProcess
import storage

#authentication 
def admin_login(username, password):
    """Admin login with hardcoded credentials."""
    if username == "admin" and password == "admin123":
        admin = Admin(id=1, username=username, password=password)
        print("Admin login successful")
        return admin
    else:
        print(" Invalid admin credentials")
        return None


#car management 
def view_all_cars():
    """View all cars in the system."""
    cars = storage.get_all_cars()
    
    if not cars:
        print("\n No cars in the system.")
        return []
    
    print(f"\n All Cars ({len(cars)}):")
    print("=" * 100)
    for car in cars:
        status = "Available" if car.available else "Unavailable"
        installment = "Yes" if car.installment else "No"
        print(f"ID: {car.id} | {car.make} {car.model} ({car.year})")
        print(f"  Price: ${car.price:,.2f} | Installment: {installment} | Status: {status} | Showroom: {car.showroom_id}")
        print("-" * 100)
    
    return cars


def add_new_car(admin_id):
    """Add a new car to the system."""
    print("\n" + "=" * 60)
    print("ADD NEW CAR")
    print("=" * 60)
    
    try:
        make = input("Car Make: ").strip()
        model = input("Car Model: ").strip()
        year = int(input("Year: ").strip())
        price = float(input("Price: ").strip())
        installment = input("Installment available? (yes/no): ").strip().lower() in ['yes', 'y']
        showroom_id = int(input("Showroom ID: ").strip())
        
        #check if showroom exists
        showroom = storage.get_showroom_by_id(showroom_id)
        if not showroom:
            print(f"\n Showroom with ID {showroom_id} not found.")
            return False
        
        car_id = storage.next_id_for("car")
        car = Car(
            id=car_id,
            make=make,
            model=model,
            year=year,
            price=price,
            installment=1 if installment else 0,
            showroom_id=showroom_id,
            available=1
        )
        
        if storage.add_car(car):
            showroom.add_car(car_id)
            storage.save_showrooms()
            
            storage.push_admin_action(admin_id, "add", "car", car_id, f"{make} {model}")
            
            print(f"\n Car added successfully Car ID: {car_id}")
            return True
        else:
            print("\n Failed to add car.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


def update_car_details():
    """Update car details."""
    print("\n" + "=" * 60)
    print("UPDATE CAR")
    print("=" * 60)
    
    try:
        car_id = int(input("Enter Car ID to update: ").strip())
        car = storage.get_car_by_id(car_id)
        
        if not car:
            print(f"\n Car with ID {car_id} not found.")
            return False
        
        print(f"\nCurrent: {car.make} {car.model} ({car.year}) - ${car.price:,.2f}")
        print("\nLeave blank to keep current value")
        
        make = input(f"New Make [{car.make}]: ").strip() or car.make
        model = input(f"New Model [{car.model}]: ").strip() or car.model
        year_input = input(f"New Year [{car.year}]: ").strip()
        year = int(year_input) if year_input else car.year
        price_input = input(f"New Price [{car.price}]: ").strip()
        price = float(price_input) if price_input else car.price
        
        if storage.update_car(car_id, make=make, model=model, year=year, price=price):
            print(f"\n Car updated successfully")
            return True
        else:
            print("\n Failed to update car.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


def delete_car_admin(admin_id):
    """Delete a car from the system."""
    try:
        car_id = int(input("Enter Car ID to delete: ").strip())
        car = storage.get_car_by_id(car_id)
        
        if not car:
            print(f"\n Car with ID {car_id} not found.")
            return False
        
        confirm = input(f"Delete {car.make} {car.model} ({car.year})? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            car_info = f"{car.make} {car.model}"
            if storage.delete_car(car_id):
                
                storage.push_admin_action(admin_id, "delete", "car", car_id, car_info)
                print(f"\n Car deleted successfully")
                return True
            else:
                print("\n Failed to delete car.")
                return False
        else:
            print("\n Deletion cancelled.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


#customer management 
def view_all_customers():
    """View all customers in the system."""
    customers = storage.get_all_customers()
    
    if not customers:
        print("\n No customers in the system.")
        return []
    
    print(f"\n All Customers ({len(customers)}):")
    print("=" * 80)
    for customer in customers:
        print(f"ID: {customer.id} | Username: {customer.username} | Phone: {customer.phone}")
        print("-" * 80)
    
    return customers


def view_customer_details(customer_id):
    """View detailed information about a specific customer."""
    customer = storage.get_customer_by_id(customer_id)
    
    if not customer:
        print(f"\n Customer with ID {customer_id} not found.")
        return None
    
    print(f"\n Customer Details (ID: {customer.id})")
    print("=" * 60)
    print(f"Username: {customer.username}")
    print(f"Phone: {customer.phone}")
    
    #transaction history
    buy_rent = storage.get_customer_buy_rent_history(customer_id)
    service = storage.get_customer_service_history(customer_id)
    reservations = storage.get_customer_reservations(customer_id)
    
    print(f"\nTransaction Summary:")
    print(f"  Purchases/Rentals: {len(buy_rent)}")
    print(f"  Services: {len(service)}")
    print(f"  Active Reservations: {len(reservations)}")
    
    total = sum(p.amount for p in buy_rent) + sum(s.amount for s in service)
    print(f"  Total Spent: ${total:,.2f}")
    print("=" * 60)
    
    return customer


def delete_customer_admin(admin_id):
    """Delete a customer from the system."""
    try:
        customer_id = int(input("Enter Customer ID to delete: ").strip())
        customer = storage.get_customer_by_id(customer_id)
        
        if not customer:
            print(f"\n Customer with ID {customer_id} not found.")
            return False
        
        confirm = input(f"Delete customer '{customer.username}'? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            if storage.delete_customer(customer_id):
                
                storage.push_admin_action(admin_id, "delete", "customer", customer_id, customer.username)
                print(f"\n Customer deleted successfully")
                return True
            else:
                print("\n Failed to delete customer.")
                return False
        else:
            print("\n Deletion cancelled.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


#showroom management
def view_all_showrooms():
    """View all showrooms in the system."""
    showrooms = storage.get_all_showrooms()
    
    if not showrooms:
        print("\n No showrooms in the system.")
        return []
    
    print(f"\n All Showrooms ({len(showrooms)}):")
    print("=" * 80)
    for showroom in showrooms:
        print(f"ID: {showroom.id} | Name: {showroom.name}")
        print(f"  Location: {showroom.location} | Phone: {showroom.phone}")
        print(f"  Cars: {len(showroom.car_ids)}")
        print("-" * 80)
    
    return showrooms


def add_new_showroom(admin_id):
    """Add a new showroom to the system."""
    print("\n" + "=" * 60)
    print("ADD NEW SHOWROOM")
    print("=" * 60)
    
    try:
        name = input("Showroom Name: ").strip()
        location = input("Location: ").strip()
        phone = input("Phone: ").strip()
        
        showroom_id = storage.next_id_for("showroom")
        showroom = Showroom(
            id=showroom_id,
            name=name,
            location=location,
            phone=phone,
            car_ids=[]
        )
        
        if storage.add_showroom(showroom):
            storage.push_admin_action(admin_id, "add", "showroom", showroom_id, name)
            print(f"\n Showroom added successfully Showroom ID: {showroom_id}")
            return True
        else:
            print("\n Failed to add showroom.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


def update_showroom_details():
    """Update showroom details."""
    print("\n" + "=" * 60)
    print("UPDATE SHOWROOM")
    print("=" * 60)
    
    try:
        showroom_id = int(input("Enter Showroom ID to update: ").strip())
        showroom = storage.get_showroom_by_id(showroom_id)
        
        if not showroom:
            print(f"\n Showroom with ID {showroom_id} not found.")
            return False
        
        print(f"\nCurrent: {showroom.name} at {showroom.location}")
        print("\nLeave blank to keep current value")
        
        name = input(f"New Name [{showroom.name}]: ").strip() or showroom.name
        location = input(f"New Location [{showroom.location}]: ").strip() or showroom.location
        phone = input(f"New Phone [{showroom.phone}]: ").strip() or showroom.phone
        
        if storage.update_showroom(showroom_id, name=name, location=location, phone=phone):
            print(f"\n Showroom updated successfully")
            return True
        else:
            print("\n Failed to update showroom.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


def delete_showroom_admin(admin_id):
    """Delete a showroom from the system."""
    try:
        showroom_id = int(input("Enter Showroom ID to delete: ").strip())
        showroom = storage.get_showroom_by_id(showroom_id)
        
        if not showroom:
            print(f"\n Showroom with ID {showroom_id} not found.")
            return False
        
        if len(showroom.car_ids) > 0:
            print(f"\n  Warning: This showroom has {len(showroom.car_ids)} car(s).")
        
        confirm = input(f"Delete showroom '{showroom.name}'? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            if storage.delete_showroom(showroom_id):
                storage.push_admin_action(admin_id, "delete", "showroom", showroom_id, showroom.name)
                print(f"\n Showroom deleted successfully")
                return True
            else:
                print("\n Failed to delete showroom.")
                return False
        else:
            print("\n Deletion cancelled.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


#garage management 
def view_all_garages():
    """View all garages in the system."""
    garages = storage.get_all_garages()
    
    if not garages:
        print("\n No garages in the system.")
        return []
    
    print(f"\n All Garages ({len(garages)}):")
    print("=" * 80)
    for garage in garages:
        print(f"ID: {garage.id} | Name: {garage.name}")
        print(f"  Location: {garage.location} | Phone: {garage.phone}")
        print(f"  Services: {len(garage.service_ids)}")
        print("-" * 80)
    
    return garages


def add_new_garage(admin_id):
    """Add a new garage to the system."""
    print("\n" + "=" * 60)
    print("ADD NEW GARAGE")
    print("=" * 60)
    
    try:
        name = input("Garage Name: ").strip()
        location = input("Location: ").strip()
        phone = input("Phone: ").strip()
        
        garage_id = storage.next_id_for("garage")
        garage = Garage(
            id=garage_id,
            name=name,
            location=location,
            phone=phone,
            service_ids=[]
        )
        
        if storage.add_garage(garage):
            storage.push_admin_action(admin_id, "add", "garage", garage_id, name)
            print(f"\n Garage added successfully Garage ID: {garage_id}")
            return True
        else:
            print("\n Failed to add garage.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


def update_garage_details():
    """Update garage details."""
    print("\n" + "=" * 60)
    print("UPDATE GARAGE")
    print("=" * 60)
    
    try:
        garage_id = int(input("Enter Garage ID to update: ").strip())
        garage = storage.get_garage_by_id(garage_id)
        
        if not garage:
            print(f"\n Garage with ID {garage_id} not found.")
            return False
        
        print(f"\nCurrent: {garage.name} at {garage.location}")
        print("\nLeave blank to keep current value")
        
        name = input(f"New Name [{garage.name}]: ").strip() or garage.name
        location = input(f"New Location [{garage.location}]: ").strip() or garage.location
        phone = input(f"New Phone [{garage.phone}]: ").strip() or garage.phone
        
        if storage.update_garage(garage_id, name=name, location=location, phone=phone):
            print(f"\n Garage updated successfully")
            return True
        else:
            print("\n Failed to update garage.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


def delete_garage_admin(admin_id):
    """Delete a garage from the system."""
    try:
        garage_id = int(input("Enter Garage ID to delete: ").strip())
        garage = storage.get_garage_by_id(garage_id)
        
        if not garage:
            print(f"\n Garage with ID {garage_id} not found.")
            return False
        
        if len(garage.service_ids) > 0:
            print(f"\n  Warning: This garage offers {len(garage.service_ids)} service(s).")
        
        confirm = input(f"Delete garage '{garage.name}'? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            if storage.delete_garage(garage_id):
                
                storage.push_admin_action(admin_id, "delete", "garage", garage_id, garage.name)
                print(f"\n Garage deleted successfully")
                return True
            else:
                print("\n Failed to delete garage.")
                return False
        else:
            print("\n Deletion cancelled.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


#service management 
def view_all_services():
    """View all services in the system."""
    services = storage.get_all_services()
    
    if not services:
        print("\n No services in the system.")
        return []
    
    print(f"\n All Services ({len(services)}):")
    print("=" * 80)
    for service in services:
        print(f"ID: {service.id} | Name: {service.name} | Price: ${service.price:.2f}")
        print("-" * 80)
    
    return services


def add_new_service(admin_id):
    """Add a new service to the system."""
    print("\n" + "=" * 60)
    print("ADD NEW SERVICE")
    print("=" * 60)
    
    try:
        name = input("Service Name: ").strip()
        price = float(input("Price: ").strip())
        
        service_id = storage.next_id_for("service")
        service = Service(
            id=service_id,
            name=name,
            price=price
        )
        
        if storage.add_service(service):
            
            storage.push_admin_action(admin_id, "add", "service", service_id, name)
            print(f"\n Service added successfully Service ID: {service_id}")
            return True
        else:
            print("\n Failed to add service.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


def update_service_details():
    """Update service details."""
    print("\n" + "=" * 60)
    print("UPDATE SERVICE")
    print("=" * 60)
    
    try:
        service_id = int(input("Enter Service ID to update: ").strip())
        service = storage.get_service_by_id(service_id)
        
        if not service:
            print(f"\n Service with ID {service_id} not found.")
            return False
        
        print(f"\nCurrent: {service.name} - ${service.price:.2f}")
        print("\nLeave blank to keep current value")
        
        name = input(f"New Name [{service.name}]: ").strip() or service.name
        price_input = input(f"New Price [{service.price}]: ").strip()
        price = float(price_input) if price_input else service.price
        
        if storage.update_service(service_id, name=name, price=price):
            print(f"\n Service updated successfully")
            return True
        else:
            print("\n Failed to update service.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


def delete_service_admin(admin_id):
    """Delete a service from the system."""
    try:
        service_id = int(input("Enter Service ID to delete: ").strip())
        service = storage.get_service_by_id(service_id)
        
        if not service:
            print(f"\n Service with ID {service_id} not found.")
            return False
        
        confirm = input(f"Delete service '{service.name}'? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            if storage.delete_service(service_id):
                
                storage.push_admin_action(admin_id, "delete", "service", service_id, service.name)
                print(f"\n Service deleted successfully")
                return True
            else:
                print("\n Failed to delete service.")
                return False
        else:
            print("\n Deletion cancelled.")
            return False
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")
        return False


#queue management 
def view_service_queue():
    """View the service request queue."""
    return storage.view_service_request_queue()


def process_next_service_request():
    """Process the next service request from the queue."""
    request = storage.dequeue_service_request()
    
    if not request:
        return None
    
    #create service process
    process_id = storage.next_id_for("service_process")
    service = storage.get_service_by_id(request['service_id'])
    
    service_process = ServiceProcess(
        process_id=process_id,
        customer_id=request['customer_id'],
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        amount=service.price if service else 0,
        service_id=request['service_id'],
        garage_id=request['garage_id']
    )
    
    storage.add_service_process(service_process)
    
    print(f"\n Service request completed")
    print(f"  Process ID: {process_id}")
    print(f"  Customer ID: {request['customer_id']}")
    if service:
        print(f"  Service: {service.name}")
        print(f"  Amount: ${service.price:.2f}")
    
    return service_process


#stack management 
def view_admin_actions():
    """View recent admin actions from the stack."""
    return storage.view_admin_action_stack()


def undo_last_action():
    """Undo the last admin action."""
    action = storage.pop_admin_action()
    
    if not action:
        return None
    
    print(f"\nUndoing action: {action['action_type']} {action['entity_type']} #{action['entity_id']}")
    
    if action['action_type'] == 'delete':
        print("  Note: Undo for delete operations requires manual restoration")
    elif action['action_type'] == 'add':
        print("  Note: Consider manually removing the added entity")
    
    print(" Action popped from stack")
    return action


#reservation management 
def view_all_reservations():
    """View all reservations in the system."""
    reservations = storage.get_all_reservations()
    
    if not reservations:
        print("\n No reservations in the system.")
        return []
    
    print(f"\n All Reservations ({len(reservations)}):")
    print("=" * 80)
    for reservation in reservations:
        customer = storage.get_customer_by_id(reservation.customer_id)
        car = storage.get_car_by_id(reservation.car_id)
        
        customer_name = customer.username if customer else f"Customer #{reservation.customer_id}"
        car_info = f"{car.make} {car.model}" if car else f"Car #{reservation.car_id}"
        
        print(f"Reservation ID: {reservation.reservation_id}")
        print(f"  Customer: {customer_name}")
        print(f"  Car: {car_info}")
        print(f"  Start: {reservation.start_time}")
        print(f"  Expires: {reservation.expiry_time}")
        print("-" * 80)
    
    return reservations


def clean_expired_reservations_admin():
    """Clean expired reservations."""
    count = storage.clean_expired_reservations()
    if count == 0:
        print("\n No expired reservations found.")
    return count


#statistics and reporting
def view_system_statistics():
    """View comprehensive system statistics."""
    print("\n" + "=" * 60)
    print("SYSTEM STATISTICS")
    print("=" * 60)
    
    print(f"\nEntities:")
    print(f"  Cars: {len(storage.get_all_cars())}")
    print(f"  Customers: {len(storage.get_all_customers())}")
    print(f"  Showrooms: {len(storage.get_all_showrooms())}")
    print(f"  Garages: {len(storage.get_all_garages())}")
    print(f"  Services: {len(storage.get_all_services())}")
    
    print(f"\nTransactions:")
    buy_rent = storage.get_all_buy_rent_processes()
    service_processes = storage.get_all_service_processes()
    print(f"  Buy/Rent Processes: {len(buy_rent)}")
    print(f"  Service Processes: {len(service_processes)}")
    
    print(f"\nQueue & Stack:")
    print(f"  Service Request Queue: {storage.get_queue_size()} pending")
    print(f"  Admin Action Stack: {storage.get_stack_size()} actions")
    
    print(f"\nReservations:")
    print(f"  Active Reservations: {len(storage.get_all_reservations())}")
    
    total_buy_rent = sum(p.amount for p in buy_rent)
    total_service = sum(p.amount for p in service_processes)
    print(f"\nRevenue:")
    print(f"  Car Sales/Rentals: ${total_buy_rent:,.2f}")
    print(f"  Services: ${total_service:,.2f}")
    print(f"  Total: ${(total_buy_rent + total_service):,.2f}")
    
    #car availability
    cars = storage.get_all_cars()
    available = sum(1 for c in cars if c.available)
    print(f"\nCar Availability:")
    print(f"  Available: {available}")
    print(f"  Unavailable: {len(cars) - available}")
    
    print("=" * 60)


#admin menu
def admin_menu(admin):
    """Main admin menu interface."""
    
    while True:
        print(f"\n{'='*60}")
        print(f" ADMIN PANEL - {admin.username}")
        print(f"{'='*60}")
        print("CAR MANAGEMENT")
        print("  1.  View All Cars")
        print("  2.  Add New Car")
        print("  3.  Update Car")
        print("  4.  Delete Car")
        print("\nCUSTOMER MANAGEMENT")
        print("  5.  View All Customers")
        print("  6.  View Customer Details")
        print("  7.  Delete Customer")
        print("\nSHOWROOM MANAGEMENT")
        print("  8.  View All Showrooms")
        print("  9.  Add New Showroom")
        print("  10. Update Showroom")
        print("  11. Delete Showroom")
        print("\nGARAGE & SERVICE MANAGEMENT")
        print("  12. View All Garages")
        print("  13. Add New Garage")
        print("  14. Update Garage")
        print("  15. Delete Garage")
        print("  16. View All Services")
        print("  17. Add New Service")
        print("  18. Update Service")
        print("  19. Delete Service")
        print("\nQUEUE & STACK OPERATIONS")
        print("  20. View Service Request Queue")
        print("  21. Process Next Service Request")
        print("  22. View Admin Action Stack")
        print("  23. Undo Last Action")
        print("\nOTHER OPERATIONS")
        print("  24. View All Reservations")
        print("  25. Clean Expired Reservations")
        print("  26. View System Statistics")
        print("  27. Save All Data")
        print("  28. Logout")
        print("=" * 60)
        
        choice = input("Enter your choice (1-28): ").strip()
        
        try:
            if choice == '1':
                view_all_cars()
            elif choice == '2':
                add_new_car(admin.id)
            elif choice == '3':
                update_car_details()
            elif choice == '4':
                delete_car_admin(admin.id)
            elif choice == '5':
                view_all_customers()
            elif choice == '6':
                customer_id = int(input("Enter Customer ID: "))
                view_customer_details(customer_id)
            elif choice == '7':
                delete_customer_admin(admin.id)
            elif choice == '8':
                view_all_showrooms()
            elif choice == '9':
                add_new_showroom(admin.id)
            elif choice == '10':
                update_showroom_details()
            elif choice == '11':
                delete_showroom_admin(admin.id)
            elif choice == '12':
                view_all_garages()
            elif choice == '13':
                add_new_garage(admin.id)
            elif choice == '14':
                update_garage_details()
            elif choice == '15':
                delete_garage_admin(admin.id)
            elif choice == '16':
                view_all_services()
            elif choice == '17':
                add_new_service(admin.id)
            elif choice == '18':
                update_service_details()
            elif choice == '19':
                delete_service_admin(admin.id)
            elif choice == '20':
                view_service_queue()
            elif choice == '21':
                process_next_service_request()
            elif choice == '22':
                view_admin_actions()
            elif choice == '23':
                undo_last_action()
            elif choice == '24':
                view_all_reservations()
            elif choice == '25':
                clean_expired_reservations_admin()
            elif choice == '26':
                view_system_statistics()
            elif choice == '27':
                storage.save_all_data()
            elif choice == '28':
                print("\n Logging out from admin panel...")
                break
            else:
                print("\n Invalid choice. Please enter a number between 1-28.")
        
        except ValueError as e:
            print(f"\n Invalid input: {e}")
        except Exception as e:
            print(f"\n An error occurred: {e}")
            print("   Please try again.")
