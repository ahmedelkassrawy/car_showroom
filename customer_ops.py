from datetime import datetime, timedelta
from models import Customer, BuyRentProcess, ServiceProcess, Reservation
import storage
import search_utils


def customer_register(username, password, phone):
    """Register a new customer account."""
    if storage.get_customer_by_username(username):
        raise ValueError("Username already exists.")
    
    id = storage.get_next_customer_id()
    customer = Customer(id = id,
                        username = username,
                        password = password,
                        phone = phone)
    customer.to_csv_row()
    if storage.add_customer(customer):
        print(f"Registration successful.Your customer id is {id}")
        return customer
    else:
        print("Registration failed. Please try again.")
        return None


def customer_login(username, password):
    """Login an existing customer."""
    if not storage.get_customer_by_username(username):
        raise ValueError("Username does not exist.")
    
    customer = storage.get_customer_by_username(username)
    if customer.check_password(password):
        print("Login successful.")
        return customer
    else:
        print("Incorrect password.")
        return None    

#######################################    

#car search
def browse_all_cars():
    """Display all available cars."""
    cars = storage.get_all_cars()

    print(f"Available Cars: {len(cars)}")
    for car in cars:
        print(car)

    return cars

def search_cars_interactive():
    """Interactive car search with filters."""
    print("\n Car Search")
    print("=" * 60)
    print("Leave blank to skip any filter\n")

    filters = {}

    make = input("Car Make (e.g., Toyota, Honda): ").strip()
    if make:
        filters['make'] = make

    model = input("Car Model (e.g., Camry, Accord): ").strip()
    if model:
        filters['model'] = model
    
    year = input("Year (e.g., 2024): ").strip()
    if year:
        try:
            filters['year'] = int(year)
        except ValueError:
            print("Invalid year, skipping")

    min_price = input("Minimum Price (e.g., 20000): ").strip()
    if min_price:
        try:
            filters['min_price'] = float(min_price)
        except ValueError:
            print("  Invalid min price, skipping")
    
    max_price = input("Maximum Price (e.g., 50000): ").strip()
    if max_price:
        try:
            filters['max_price'] = float(max_price)
        except ValueError:
            print("  Invalid max price, skipping")
    
    installment = input("Installment available (yes/no): ").strip().lower()
    if installment in ['yes', 'y','YES']:
        filters['installment'] = 1
    elif installment in ['no', 'n', 'NO']:
        filters['installment'] = 0
    

    filters['available_only'] = True
    results = search_utils.general_car_search(filters)

    if not results:
        print("No cars found matching the criteria.")
        return []
    
    print(f"\n Found {len(results)} car(s):")
    print("=" * 100)
    for i, car in enumerate(results, 1):
        installment_text = " Installment" if car.installment else "Cash Only"
        print(f"{i}. ID: {car.id} | {car.make} {car.model} ({car.year})")
        print(f"  ${car.price:,.2f} | {installment_text}")
        print("-" * 100)
    
    return results


def view_car_details(car_id):
    """Display detailed information about a specific car."""
    car = storage.get_car_by_id(car_id)
    
    if not car:
        print(f" Car with ID {car_id} not found.")
        return None
    
    print(f"\n Car Details (ID: {car.id})")
    print("=" * 60)
    print(f"Make: {car.make}")
    print(f"Model: {car.model}")
    print(f"Year: {car.year}")
    print(f"Price: ${car.price:,.2f}")
    print(f"Installment: {'Available' if car.installment else 'Not Available'}")
    print(f"Showroom ID: {car.showroom_id}")
    print(f"Status: {'Available' if car.available else 'Not Available'}")
    print("=" * 60)
    
    return car


def view_showrooms():
    """Display all showrooms."""
    showrooms = storage.get_all_showrooms()
    
    if not showrooms:
        print("\n No showrooms available.")
        return []
    
    print(f"\n Available Showrooms ({len(showrooms)}):")
    print("=" * 80)
    for showroom in showrooms:
        car_count = len(showroom.car_ids)

        print(f"ID: {showroom.id} | {showroom.name}")
        print(f"Location: {showroom.location}")
        print(f"Phone: {showroom.phone}")
        print(f"Cars: {car_count}")
        print("-" * 80)
    
    return showrooms


def view_cars_in_showroom(showroom_id):
    """Display all cars in a specific showroom."""
    showroom = storage.get_showroom_by_id(showroom_id)

    if not showroom:
        print(f" Showroom with ID {showroom_id} not found.")
        return []

    cars = storage.get_cars_in_showroom(showroom_id)

    if not cars:
        print(f"\n No cars available in showroom ID {showroom_id}.")
        return []

    available_cars = [car for car in cars if car.available]
    
    print(f"\n Showroom Name: {showroom.name}")
    print(f"Location: {showroom.location}")
    print(f"Cars ({len(available_cars)} available / {len(cars)} total):")
    print("=" * 80)
    
    if not available_cars:
        print("No available cars in this showroom.")
        return []
    
    for car in available_cars:
        print(f"ID: {car.id} | {car.make} {car.model} ({car.year}) - ${car.price:,.2f}")
        print("-" * 80)
    
    return available_cars
    

def view_garages():
    """Display all garages."""
    garages = storage.get_all_garages()
    
    if not garages:
        print("\n No garages available.")
        return []
    
    print(f"\n Available Garages ({len(garages)}):")
    print("=" * 80)
    for garage in garages:
        service_count = len(garage.service_ids)
        print(f"ID: {garage.id} | {garage.name}")
        print(f"Location: {garage.location}")
        print(f"Phone: {garage.phone}")
        print(f"Services: {service_count}")
        print("-" * 80)
    
    return garage


def view_services_in_garage(garage_id):
    """Display all services in a specific garage."""
    garage = storage.get_garage_by_id(garage_id)

    if not garage:
        print(f" Garage with ID {garage_id} not found.")
        return []
    
    services = storage.get_services_in_garage(garage_id)

    if not services:
        print(f"\n No services available in garage ID {garage_id}.")
        return []
    
    print(f"\n Garage Name: {garage.name}")
    print(f"Location: {garage.location}")
    print(f"Available Services ({len(services)}):")
    print("=" * 60)
    
    if not services:
        print("No services available in this garage.")
        return []
    
    for service in services:
        print(f"ID: {service.id} | {service.name} - ${service.price:.2f}")
        print("-" * 60)
    
    return services


#car purchase 
def buy_car(customer_id, car_id):
    """Process a car purchase."""
    #get car 
    car = storage.get_car_by_id(car_id)

    if not car:
        print(f" Car with ID {car_id} not found.")
        return False
    
    if not car.available:
        print(f" Car with ID {car_id} is not available for purchase.")
        return False
    
    process_id = storage.next_id_for('buy_rent_process')
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    buy_process = BuyRentProcess(
        process_id = process_id,
        customer_id = customer_id,
        date = date,
        amount = car.price,
        car_id = car_id,
        type = "buy"
    )

    storage.add_buy_rent_process(buy_process)
    storage.update_car(car_id, available=0)

    print(f"\n Congratulations You have successfully purchased:")
    print(f" {car.make} {car.model} ({car.year})")
    print(f" Amount Paid: ${car.price:,.2f}")
    print(f" Date: {date}")
    print(f" Transaction ID: {process_id}")
    
    return True


def rent_car(customer_id, car_id):
    """Process a car rental."""
    car = storage.get_car_by_id(car_id)

    if not car:
        print(f" Car with ID {car_id} not found.")
        return False
    
    if not car.available:
        print(f" Car with ID {car_id} is not available for purchase.")
        return False
    
    rent_amount = car.price * 0.1
    process_id = storage.next_id_for('buy_rent_process')
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    rent_process = BuyRentProcess(
        process_id = process_id,
        customer_id = customer_id,
        date = date,
        amount = rent_amount,
        car_id = car_id,
        type = "rent"
    )

    storage.add_buy_rent_process(rent_process)
    storage.update_car(car_id, available=0)

    print(f"\n Congratulations. You have successfully rented:")
    print(f"{car.make} {car.model} ({car.year})")
    print(f"Rent Amount: ${rent_amount:,.2f}")
    print(f"Date: {date}")
    print(f"Transaction ID: {process_id}")
    
    return True


def reserve_car(customer_id, car_id, hours=24):
    """Reserve a car for a specified duration."""
    car = storage.get_car_by_id(car_id)

    if not car:
        print(f" Car with ID {car_id} not found.")
        return False
    
    if not car.available:
        print(f" Car with ID {car_id} is not available for purchase.")
        return False
    
    reservation_id = storage.next_id_for("reservation")
    
    start = datetime.now()
    expiry = start + timedelta(hours=hours)

    reservation = Reservation(
        reservation_id = reservation_id,
        customer_id = customer_id,
        car_id = car_id,
        start_time = start.strftime('%Y-%m-%d %H:%M:%S'),
        expiry_time = expiry.strftime('%Y-%m-%d %H:%M:%S')
    )

    storage.add_reservation(reservation)
    storage.update_car(car_id, available=0)

    print(f"\n Car reserved successfully!")
    print(f" {car.make} {car.model} ({car.year})")
    print(f" Duration: {hours} hour(s)")
    print(f" Expires: {expiry.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Reservation ID: {reservation_id}")
    print(f"\n  Please complete your purchase within {hours} hours!")
    
    return True


def cancel_reservation(customer_id, reservation_id):
    """Cancel car reservation."""
    reservation = storage.get_reservation_by_id(reservation_id)

    if not reservation:
        print(f" Reservation with ID {reservation_id} not found.")
        return False
    
    if reservation.customer_id != customer_id:
        print(" You can only cancel your own reservations.")
        return False
    
    storage.delete_reservation(reservation_id)
    car = storage.get_car_by_id(reservation.car_id)
    storage.update_car(car.id, available=1)

    print(f"\nReservation cancelled successfully")
    if car.id:
        print(f"{car.make} {car.model} is now available")
    
    return True


def view_my_service_requests(customer_id):
    """View customer's service requests in the queue."""
    queue = storage.service_request_queue
    
    customer_requests = [req for req in queue if req['customer_id'] == customer_id]
    
    if not customer_requests:
        print("\n You have no pending service requests in the queue.")
        return []
    
    print(f"\n Your Service Requests ({len(customer_requests)} pending):")
    print("=" * 80)
    
    for req in customer_requests:
        service = storage.get_service_by_id(req['service_id'])
        garage = storage.get_garage_by_id(req['garage_id'])
        position = queue.index(req) + 1
        
        service_name = service.name if service else f"Service #{req['service_id']}"
        garage_name = garage.name if garage else f"Garage #{req['garage_id']}"
        
        print(f"Request #{req['request_id']}")
        print(f"Position in Queue: {position}")
        print(f"Service: {service_name}")
        print(f"Garage: {garage_name}")
        print(f"Status: {req['status']}")
        print(f"Requested: {req['timestamp']}")
        print("-" * 80)
    
    return customer_requests


def book_service(customer_id, service_id, garage_id):
    """Book a service at a garage by adding to service request queue."""
    service = storage.get_service_by_id(service_id)

    if not service:
        print(f"Service with ID {service_id} not found.")
        return False

    garage = storage.get_garage_by_id(garage_id)

    if not garage:
        print(f"Garage with ID {garage_id} not found.")
        return False

    if service_id not in garage.service_ids:
        print(f"Service ID {service_id} is not offered at Garage ID {garage_id}.")
        return False
    
    request_id = storage.enqueue_service_request(customer_id, service_id, garage_id)
    queue_position = storage.get_queue_size()

    print(f"\n Service request submitted successfully")
    print(f" Service: {service.name}")
    print(f" Garage: {garage.name}")
    print(f" Location: {garage.location}")
    print(f" Estimated Price: ${service.price:.2f}")
    print(f" Request ID: {request_id}")
    print(f" Queue Position: {queue_position}")
    print(f"\n Your service will be processed in order. Check your queue status")
    
    return True

#history and profile
def view_customer_history(customer_id):
    """Display customer's complete transaction history."""

    customer = storage.get_customer_by_id(customer_id)
    
    if not customer:
        print(f"Customer with ID {customer_id} not found.")
        return
    
    buy_rent_processes = storage.get_customer_buy_rent_history(customer_id)
    service_processes = storage.get_customer_service_history(customer_id)
    
    print(f"\n{'='*80}")
    print(f" Transaction History for {customer.username} (ID: {customer_id})")
    print(f"{'='*80}")
    
    if buy_rent_processes:
        print(f"\n Car Purchases & Rentals ({len(buy_rent_processes)}):")
        print("-" * 80)
        
        for process in buy_rent_processes:
            car = storage.get_car_by_id(process.car_id)
            car_info = f"{car.make} {car.model} ({car.year})" if car else f"Car ID: {process.car_id}"
            
            print(f"Process ID: {process.process_id}")
            print(f"Type: {process.type.upper()}")
            print(f"Car: {car_info}")
            print(f"Amount: ${process.amount:,.2f}")
            print(f"Date: {process.date}")
            print("-" * 80)
    else:
        print("\n Car Purchases & Rentals: No transactions found")
    
    if service_processes:
        print(f"\n Service History ({len(service_processes)}):")
        print("-" * 80)
        
        for process in service_processes:
            service = storage.get_service_by_id(process.service_id)
            garage = storage.get_garage_by_id(process.garage_id)
            
            service_name = service.name if service else f"Service ID: {process.service_id}"
            garage_name = garage.name if garage else f"Garage ID: {process.garage_id}"
            
            print(f"Process ID: {process.process_id}")
            print(f"Service: {service_name}")
            print(f"Garage: {garage_name}")
            print(f"Amount: ${process.amount:,.2f}")
            print(f"Date: {process.date}")
            print("-" * 80)
    else:
        print("\n Service History: No transactions found")
    
    # summary
    total_buy_rent = sum(p.amount for p in buy_rent_processes)
    total_service = sum(p.amount for p in service_processes)
    total_spent = total_buy_rent + total_service
    
    print(f"\n Summary:")
    print(f"Total Car Purchases/Rentals: ${total_buy_rent:,.2f}")
    print(f"Total Services: ${total_service:,.2f}")
    print(f"Total Spent: ${total_spent:,.2f}")
    print("=" * 80)

#customer menu
def customer_menu(customer):
    """Main customer menu interface."""
    
    while True:
        print(f"\n{'='*60}")
        print(f" Welcome, {customer.username}")
        print(f"{'='*60}")
        print("1.  Browse All Available Cars")
        print("2.  Search Cars (Advanced)")
        print("3.  View Car Details")
        print("4.  View Showrooms")
        print("5.  View Cars in Showroom")
        print("6.  View Garages")
        print("7.  View Services in Garage")
        print("8.  Buy a Car")
        print("9.  Rent a Car")
        print("10. Reserve a Car")
        print("11. Cancel Reservation")
        print("12. Book a Service")
        print("13. View My Service Requests (Queue)")
        print("14. View My History")
        print("15. Logout")
        print("=" * 60)
        
        choice = input("Enter your choice (1-15): ").strip()
        
        try:
            if choice == '1':
                browse_all_cars()
            
            elif choice == '2':
                search_cars_interactive()
            
            elif choice == '3':
                car_id = int(input("Enter Car ID: "))
                view_car_details(car_id)
            
            elif choice == '4':
                view_showrooms()
            
            elif choice == '5':
                showroom_id = int(input("Enter Showroom ID: "))
                view_cars_in_showroom(showroom_id)
            
            elif choice == '6':
                view_garages()
            
            elif choice == '7':
                garage_id = int(input("Enter Garage ID: "))
                view_services_in_garage(garage_id)
            
            elif choice == '8':
                car_id = int(input("Enter Car ID to buy: "))
                buy_car(customer.id, car_id)
            
            elif choice == '9':
                car_id = int(input("Enter Car ID to rent: "))
                rent_car(customer.id, car_id)
            
            elif choice == '10':
                car_id = int(input("Enter Car ID to reserve: "))
                hours = int(input("Reservation duration in hours (default 24): ") or "24")
                reserve_car(customer.id, car_id, hours)
            
            elif choice == '11':
                reservation_id = int(input("Enter Reservation ID to cancel: "))
                cancel_reservation(customer.id, reservation_id)
            
            elif choice == '12':
                service_id = int(input("Enter Service ID: "))
                garage_id = int(input("Enter Garage ID: "))
                book_service(customer.id, service_id, garage_id)
            
            elif choice == '13':
                view_my_service_requests(customer.id)
            
            elif choice == '14':
                view_customer_history(customer.id)
            
            elif choice == '15':
                print("\n Logging out Goodbye")
                break
            
            else:
                print("\n Invalid choice. Please enter a number between 1-15.")
        
        except ValueError as e:
            print(f"\n Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"\n An error occurred: {e}")
            print("   Please try again.")


def main_customer_flow():
    """Main customer authentication and menu flow."""
    while True:
        print("\n" + "=" * 60)
        print("CAR SHOWROOM - CUSTOMER PORTAL")
        print("=" * 60)
        print("1. Register New Account")
        print("2. Login")
        print("3. Exit")
        print("=" * 60)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\n Customer Registration")
            print("-" * 60)
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            phone = input("Phone Number: ").strip()
            
            if username and password and phone:
                customer = customer_register(username, password, phone)
                if customer:
                    input("\nPress Enter to continue to login")
            else:
                print("All fields are required")
        
        elif choice == '2':
            print("\n Customer Login")
            print("-" * 60)
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            if username and password:
                customer = customer_login(username, password)
                if customer:
                    customer_menu(customer)
            else:
                print("Username and password are required")
        
        elif choice == '3':
            print("\n Thank you for visiting Goodbye")
            break
        
        else:
            print("\n Invalid choice. Please enter 1, 2, or 3.")






