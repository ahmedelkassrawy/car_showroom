import sys
import storage
import customer_ops
from models import Admin


#admin authentication
def admin_login():
    """Admin login with hardcoded credentials."""
    print("\n" + "=" * 60)
    print("ADMIN LOGIN")
    print("=" * 60)
    
    username = input("Admin Username: ").strip()
    password = input("Admin Password: ").strip()
    
    if username == "admin" and password == "admin123":
        admin = Admin(id=1, username=username, password=password)
        print("\n Admin login successful")
        return admin
    else:
        print("\n Invalid admin credentials")
        return None


#admin menu
def admin_menu(admin):
    """Main admin menu interface."""
    
    while True:
        print(f"\n{'='*60}")
        print(f" ADMIN PANEL - {admin.username}")
        print(f"{'='*60}")
        print("1.  View All Cars")
        print("2.  Add New Car")
        print("3.  Update Car")
        print("4.  Delete Car")
        print("5.  View All Customers")
        print("6.  View All Showrooms")
        print("7.  Add New Showroom")
        print("8.  View All Garages")
        print("9.  Add New Garage")
        print("10. View All Services")
        print("11. Add New Service")
        print("12. View Service Request Queue")
        print("13. Process Next Service Request")
        print("14. View Admin Action Stack")
        print("15. Undo Last Action")
        print("16. View All Reservations")
        print("17. Clean Expired Reservations")
        print("18. View Statistics")
        print("19. Save All Data")
        print("20. Logout")
        print("=" * 60)
        
        choice = input("Enter your choice (1-20): ").strip()
        
        try:
            if choice == '1':
                view_all_cars()
            
            elif choice == '2':
                add_new_car(admin.id)
            
            elif choice == '3':
                update_car_admin()
            
            elif choice == '4':
                delete_car_admin(admin.id)
            
            elif choice == '5':
                view_all_customers()
            
            elif choice == '6':
                view_all_showrooms()
            
            elif choice == '7':
                add_new_showroom(admin.id)
            
            elif choice == '8':
                view_all_garages()
            
            elif choice == '9':
                add_new_garage(admin.id)
            
            elif choice == '10':
                view_all_services()
            
            elif choice == '11':
                add_new_service(admin.id)
            
            elif choice == '12':
                storage.view_service_request_queue()
            
            elif choice == '13':
                process_next_service_request()
            
            elif choice == '14':
                storage.view_admin_action_stack()
            
            elif choice == '15':
                undo_last_action()
            
            elif choice == '16':
                view_all_reservations()
            
            elif choice == '17':
                storage.clean_expired_reservations()
            
            elif choice == '18':
                view_statistics()
            
            elif choice == '19':
                storage.save_all_data()
            
            elif choice == '20':
                print("\n Logging out from admin panel")
                break
            
            else:
                print("\n Invalid choice. Please enter a number between 1-20.")
        
        except ValueError as e:
            print(f"\n Invalid input: {e}")
        except Exception as e:
            print(f"\n An error occurred: {e}")
            print("   Please try again.")


#admin operations
def view_all_cars():
    """View all cars in the system."""
    cars = storage.get_all_cars()
    
    if not cars:
        print("\n No cars in the system.")
        return
    
    print(f"\n All Cars ({len(cars)}):")
    print("=" * 100)
    for car in cars:
        status = "Available" if car.available else "Unavailable"
        installment = "Yes" if car.installment else "No"
        print(f"ID: {car.id} | {car.make} {car.model} ({car.year})")
        print(f"  Price: ${car.price:,.2f} | Installment: {installment} | Status: {status} | Showroom: {car.showroom_id}")
        print("-" * 100)


def add_new_car(admin_id):
    """Add a new car to the system."""
    from models import Car
    
    print("\n" + "=" * 60)
    print("ADD NEW CAR")
    print("=" * 60)
    
    try:
        make = input("Car Make: ").strip()
        model = input("Car Model: ").strip()
        year = int(input("Year: ").strip())
        price = float(input("Price: ").strip())
        installment = input("Installment available (yes/no): ").strip().lower() in ['yes', 'y']
        showroom_id = int(input("Showroom ID: ").strip())
        
        #check if showroom exists
        showroom = storage.get_showroom_by_id(showroom_id)
        if not showroom:
            print(f"\n Showroom with ID {showroom_id} not found.")
            return
        
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
        else:
            print("\n Failed to add car.")
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")


def update_car_admin():
    """Update car details."""
    print("\n" + "=" * 60)
    print("UPDATE CAR")
    print("=" * 60)
    
    try:
        car_id = int(input("Enter Car ID to update: ").strip())
        car = storage.get_car_by_id(car_id)
        
        if not car:
            print(f"\n Car with ID {car_id} not found.")
            return
        
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
        else:
            print("\n Failed to update car.")
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")


def delete_car_admin(admin_id):
    """Delete a car from the system."""
    try:
        car_id = int(input("Enter Car ID to delete: ").strip())
        car = storage.get_car_by_id(car_id)
        
        if not car:
            print(f"\n Car with ID {car_id} not found.")
            return
        
        confirm = input(f"Delete {car.make} {car.model} ({car.year})? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            car_info = f"{car.make} {car.model}"
            if storage.delete_car(car_id):
                
                storage.push_admin_action(admin_id, "delete", "car", car_id, car_info)
                print(f"\n Car deleted successfully")
            else:
                print("\n Failed to delete car.")
        else:
            print("\n Deletion cancelled.")
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")


#admin operations - customers
def view_all_customers():
    """View all customers in the system."""
    customers = storage.get_all_customers()
    
    if not customers:
        print("\n No customers in the system.")
        return
    
    print(f"\n All Customers ({len(customers)}):")
    print("=" * 80)
    for customer in customers:
        print(f"ID: {customer.id} | Username: {customer.username} | Phone: {customer.phone}")
        print("-" * 80)


#admin operations - showrooms
def view_all_showrooms():
    """View all showrooms in the system."""
    showrooms = storage.get_all_showrooms()
    
    if not showrooms:
        print("\n No showrooms in the system.")
        return
    
    print(f"\n All Showrooms ({len(showrooms)}):")
    print("=" * 80)
    for showroom in showrooms:
        print(f"ID: {showroom.id} | Name: {showroom.name}")
        print(f"  Location: {showroom.location} | Phone: {showroom.phone}")
        print(f"  Cars: {len(showroom.car_ids)}")
        print("-" * 80)


def add_new_showroom(admin_id):
    """Add a new showroom to the system."""
    from models import Showroom
    
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
        else:
            print("\n Failed to add showroom.")
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")


#admin operations - garages
def view_all_garages():
    """View all garages in the system."""
    garages = storage.get_all_garages()
    
    if not garages:
        print("\n No garages in the system.")
        return
    
    print(f"\n All Garages ({len(garages)}):")
    print("=" * 80)
    for garage in garages:
        print(f"ID: {garage.id} | Name: {garage.name}")
        print(f"  Location: {garage.location} | Phone: {garage.phone}")
        print(f"  Services: {len(garage.service_ids)}")
        print("-" * 80)


def add_new_garage(admin_id):
    """Add a new garage to the system."""
    from models import Garage
    
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
        else:
            print("\n Failed to add garage.")
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")


#admin operations - services
def view_all_services():
    """View all services in the system."""
    services = storage.get_all_services()
    
    if not services:
        print("\n No services in the system.")
        return
    
    print(f"\n All Services ({len(services)}):")
    print("=" * 80)
    for service in services:
        print(f"ID: {service.id} | Name: {service.name} | Price: ${service.price:.2f}")
        print("-" * 80)


def add_new_service(admin_id):
    """Add a new service to the system."""
    from models import Service
    
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
        else:
            print("\n Failed to add service.")
    
    except ValueError as e:
        print(f"\n Invalid input: {e}")


#admin operations - queue management
def process_next_service_request():
    """Process the next service request from the queue."""
    from models import ServiceProcess
    from datetime import datetime
    
    request = storage.dequeue_service_request()
    
    if not request:
        return
    
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


#admin operations
def undo_last_action():
    """Undo the last admin action."""
    action = storage.pop_admin_action()
    
    if not action:
        return
    
    print(f"\nUndoing action: {action['action_type']} {action['entity_type']} #{action['entity_id']}")
    
    if action['action_type'] == 'delete' and action['entity_type'] == 'car':
        print("Note: Undo for delete operations requires manual restoration")
    
    print(" Action popped from stack")


#reservations
def view_all_reservations():
    """View all reservations in the system."""
    reservations = storage.get_all_reservations()
    
    if not reservations:
        print("\n No reservations in the system.")
        return
    
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


#statistics
def view_statistics():
    """View system statistics."""
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
    
    #revenue
    total_buy_rent = sum(p.amount for p in buy_rent)
    total_service = sum(p.amount for p in service_processes)
    print(f"\nRevenue:")
    print(f"  Car Sales/Rentals: ${total_buy_rent:,.2f}")
    print(f"  Services: ${total_service:,.2f}")
    print(f"  Total: ${(total_buy_rent + total_service):,.2f}")
    print("=" * 60)


#main menu
def main_menu():
    """Main application menu."""
    while True:
        print("\n" + "=" * 60)
        print("CAR SHOWROOM MANAGEMENT SYSTEM")
        print("=" * 60)
        print("1. Customer Portal")
        print("2. Admin Panel")
        print("3. Exit")
        print("=" * 60)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            customer_ops.main_customer_flow()
        
        elif choice == '2':
            admin = admin_login()
            if admin:
                admin_menu(admin)
        
        elif choice == '3':
            print("\n" + "=" * 60)
            print("Saving data before exit")
            storage.save_all_data()
            print("Thank you for using Car Showroom Management System")
            print("=" * 60)
            break
        
        else:
            print("\n Invalid choice. Please enter 1, 2, or 3.")



if __name__ == "__main__":
    try:
        print("\n" + "=" * 60)
        print("INITIALIZING CAR SHOWROOM MANAGEMENT SYSTEM")
        print("=" * 60)
        
        storage.load_all_data()
        
        print("\n System initialized successfully")
        
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("System interrupted by user")
        print("Saving data")
        storage.save_all_data()
        print("=" * 60)
        sys.exit(0)
    
    except Exception as e:
        print(f"\n Fatal error: {e}")
        print("Attempting to save data")
        try:
            storage.save_all_data()
            print(" Data saved successfully")
        except:
            print(" Failed to save data")
        sys.exit(1)
