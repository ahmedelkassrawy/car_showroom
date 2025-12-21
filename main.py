import sys
import storage
import customer_ops
import admin_ops
from models import Admin


#admin authentication
def admin_login():
    """Admin login with hardcoded credentials."""
    print("\n" + "=" * 60)
    print("ADMIN LOGIN")
    print("=" * 60)
    
    username = input("Admin Username: ").strip()
    password = input("Admin Password: ").strip()
    
    admin = admin_ops.admin_login(username, password)
    if admin:
        print("\n Admin login successful")
    else:
        print("\n Invalid admin credentials")
    return admin


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
                admin_ops.view_all_cars()
            
            elif choice == '2':
                admin_ops.add_new_car(admin.id)
            
            elif choice == '3':
                admin_ops.update_car_details()
            
            elif choice == '4':
                admin_ops.delete_car_admin(admin.id)
            
            elif choice == '5':
                admin_ops.view_all_customers()
            
            elif choice == '6':
                admin_ops.view_all_showrooms()
            
            elif choice == '7':
                admin_ops.add_new_showroom(admin.id)
            
            elif choice == '8':
                admin_ops.view_all_garages()
            
            elif choice == '9':
                admin_ops.add_new_garage(admin.id)
            
            elif choice == '10':
                admin_ops.view_all_services()
            
            elif choice == '11':
                admin_ops.add_new_service(admin.id)
            
            elif choice == '12':
                admin_ops.view_service_queue()
            
            elif choice == '13':
                admin_ops.process_next_service_request()
            
            elif choice == '14':
                admin_ops.view_admin_actions()
            
            elif choice == '15':
                admin_ops.undo_last_action()
            
            elif choice == '16':
                admin_ops.view_all_reservations()
            
            elif choice == '17':
                storage.clean_expired_reservations()
            
            elif choice == '18':
                admin_ops.view_system_statistics()
            
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
