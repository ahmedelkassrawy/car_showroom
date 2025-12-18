import tkinter as tk
from tkinter import ttk, messagebox
import storage
import models
from datetime import datetime

storage.ensure_data_directory()

try:
    storage.load_all_data()
except Exception as e:
    print(f"Error loading data: {e}")

class CarShowroomApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Car Showroom Management System")
        self.geometry("1000x700")
        
        self.current_user = None
        self.user_type = None #admin or customer

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.frames = {}
        
        self.show_frame("LoginScreen")

    def show_frame(self, frame_name, **kwargs):
        #clear container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        if frame_name == "LoginScreen":
            frame = LoginScreen(self.container, self)
        elif frame_name == "AdminDashboard":
            frame = AdminDashboard(self.container, self)
        elif frame_name == "CustomerDashboard":
            frame = CustomerDashboard(self.container, self)
        elif frame_name == "RegisterScreen":
            frame = RegisterScreen(self.container, self)
        else:
            return

        frame.pack(fill="both", expand=True)

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Center the login box
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(self, text="Car Showroom System", font=("Helvetica", 24, "bold")).pack(pady=20)
        
        # Login Form
        login_frame = tk.LabelFrame(self, text="Login", padx=20, pady=20)
        login_frame.pack(padx=20, pady=10)
        
        tk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Button(login_frame, text="Login", command=self.login, width=20, bg="#007bff", fg="white").grid(row=2, column=0, columnspan=2, pady=15)
        
        tk.Button(self, text="Create New Customer Account", command=lambda: controller.show_frame("RegisterScreen")).pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Admin Login (Hardcoded as per admin_ops.py)
        if username == "admin" and password == "admin123":
            self.controller.current_user = models.Admin(id=1, username=username, password=password)
            self.controller.user_type = 'admin'
            self.controller.show_frame("AdminDashboard")
            return

        # Customer Login
        customer = storage.get_customer_by_username(username)
        if customer and customer.check_password(password):
            self.controller.current_user = customer
            self.controller.user_type = 'customer'
            self.controller.show_frame("CustomerDashboard")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class RegisterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(self, text="Register New Customer", font=("Helvetica", 18)).pack(pady=20)
        
        form_frame = tk.Frame(self)
        form_frame.pack(padx=20, pady=10)
        
        tk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Phone:").grid(row=2, column=0, sticky="e", pady=5)
        self.phone_entry = tk.Entry(form_frame)
        self.phone_entry.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Button(form_frame, text="Register", command=self.register, width=20, bg="#28a745", fg="white").grid(row=3, column=0, columnspan=2, pady=15)
        tk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginScreen")).pack()

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not username or not password or not phone:
            messagebox.showerror("Error", "All fields are required")
            return
            
        if storage.get_customer_by_username(username):
            messagebox.showerror("Error", "Username already exists")
            return
            
        customer_id = storage.get_next_customer_id()
        new_customer = models.Customer(id=customer_id, username=username, password=password, phone=phone)
        
        if storage.add_customer(new_customer):
            messagebox.showinfo("Success", f"Registration successful! Your ID is {customer_id}")
            self.controller.show_frame("LoginScreen")
        else:
            messagebox.showerror("Error", "Registration failed")

class AdminDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg="#343a40", height=50)
        header.pack(fill="x")
        tk.Label(header, text=f"Admin Dashboard - {controller.current_user.username}", bg="#343a40", fg="white", font=("Helvetica", 12)).pack(side="left", padx=20, pady=10)
        tk.Button(header, text="Logout", command=lambda: controller.show_frame("LoginScreen"), bg="#dc3545", fg="white").pack(side="right", padx=20, pady=10)
        
        # Main Content
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.cars_tab = CarsTab(self.notebook, controller)
        self.notebook.add(self.cars_tab, text="Cars")
        
        self.customers_tab = CustomersTab(self.notebook, controller)
        self.notebook.add(self.customers_tab, text="Customers")

        self.showrooms_tab = ShowroomsTab(self.notebook, controller)
        self.notebook.add(self.showrooms_tab, text="Showrooms")

        self.garages_tab = GaragesTab(self.notebook, controller)
        self.notebook.add(self.garages_tab, text="Garages")
        
        self.services_tab = ServicesTab(self.notebook, controller)
        self.notebook.add(self.services_tab, text="Services")

        self.reservations_tab = ReservationsTab(self.notebook, controller)
        self.notebook.add(self.reservations_tab, text="Reservations")

        self.service_queue_tab = ServiceQueueTab(self.notebook, controller)
        self.notebook.add(self.service_queue_tab, text="Service Queue")

        self.statistics_tab = StatisticsTab(self.notebook, controller)
        self.notebook.add(self.statistics_tab, text="Statistics")

class CarsTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Toolbar
        toolbar = tk.Frame(self)
        toolbar.pack(fill="x", padx=5, pady=5)
        tk.Button(toolbar, text="Refresh", command=self.load_cars).pack(side="left", padx=5)
        tk.Button(toolbar, text="Add Car", command=self.add_car_dialog).pack(side="left", padx=5)
        tk.Button(toolbar, text="Update Car", command=self.update_car_dialog).pack(side="left", padx=5)
        tk.Button(toolbar, text="Delete Selected", command=self.delete_car).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Make", "Model", "Year", "Price", "Status", "Showroom")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_cars()

    def load_cars(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        cars = storage.get_all_cars()
        for car in cars:
            status = "Available" if car.available else "Unavailable"
            self.tree.insert("", "end", values=(car.id, car.make, car.model, car.year, f"${car.price:,.2f}", status, car.showroom_id))

    def add_car_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add New Car")
        dialog.geometry("400x400")
        
        tk.Label(dialog, text="Make:").pack(pady=5)
        make_entry = tk.Entry(dialog)
        make_entry.pack(pady=5)
        
        tk.Label(dialog, text="Model:").pack(pady=5)
        model_entry = tk.Entry(dialog)
        model_entry.pack(pady=5)
        
        tk.Label(dialog, text="Year:").pack(pady=5)
        year_entry = tk.Entry(dialog)
        year_entry.pack(pady=5)
        
        tk.Label(dialog, text="Price:").pack(pady=5)
        price_entry = tk.Entry(dialog)
        price_entry.pack(pady=5)
        
        tk.Label(dialog, text="Showroom ID:").pack(pady=5)
        showroom_entry = tk.Entry(dialog)
        showroom_entry.pack(pady=5)
        
        installment_var = tk.BooleanVar()
        tk.Checkbutton(dialog, text="Installment Available", variable=installment_var).pack(pady=5)
        
        def save():
            try:
                make = make_entry.get()
                model = model_entry.get()
                year = int(year_entry.get())
                price = float(price_entry.get())
                showroom_id = int(showroom_entry.get())
                
                if not storage.get_showroom_by_id(showroom_id):
                    messagebox.showerror("Error", "Showroom ID not found")
                    return

                car_id = storage.next_id_for("car")
                car = models.Car(
                    id=car_id,
                    make=make,
                    model=model,
                    year=year,
                    price=price,
                    installment=1 if installment_var.get() else 0,
                    showroom_id=showroom_id,
                    available=1
                )
                
                if storage.add_car(car):
                    showroom = storage.get_showroom_by_id(showroom_id)
                    showroom.add_car(car_id)
                    storage.save_showrooms()
                    storage.push_admin_action(self.controller.current_user.id, "add", "car", car_id, f"{make} {model}")
                    
                    messagebox.showinfo("Success", "Car added successfully")
                    self.load_cars()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to add car")
            except ValueError:
                messagebox.showerror("Error", "Invalid input")

        tk.Button(dialog, text="Save", command=save).pack(pady=20)

    def update_car_dialog(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        car_id = int(item['values'][0])
        car = storage.get_car_by_id(car_id)
        
        dialog = tk.Toplevel(self)
        dialog.title("Update Car")
        dialog.geometry("400x400")
        
        tk.Label(dialog, text="Make:").pack(pady=5)
        make_entry = tk.Entry(dialog)
        make_entry.insert(0, car.make)
        make_entry.pack(pady=5)
        
        tk.Label(dialog, text="Model:").pack(pady=5)
        model_entry = tk.Entry(dialog)
        model_entry.insert(0, car.model)
        model_entry.pack(pady=5)
        
        tk.Label(dialog, text="Year:").pack(pady=5)
        year_entry = tk.Entry(dialog)
        year_entry.insert(0, str(car.year))
        year_entry.pack(pady=5)
        
        tk.Label(dialog, text="Price:").pack(pady=5)
        price_entry = tk.Entry(dialog)
        price_entry.insert(0, str(car.price))
        price_entry.pack(pady=5)
        
        def save():
            try:
                make = make_entry.get()
                model = model_entry.get()
                year = int(year_entry.get())
                price = float(price_entry.get())
                
                if storage.update_car(car_id, make=make, model=model, year=year, price=price):
                    messagebox.showinfo("Success", "Car updated successfully")
                    self.load_cars()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update car")
            except ValueError:
                messagebox.showerror("Error", "Invalid input")

        tk.Button(dialog, text="Update", command=save).pack(pady=20)

    def delete_car(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        car_id = int(item['values'][0])
        
        if messagebox.askyesno("Confirm", f"Delete car ID {car_id}?"):
            if storage.delete_car(car_id):
                storage.push_admin_action(self.controller.current_user.id, "delete", "car", car_id, "Deleted Car")
                self.load_cars()
            else:
                messagebox.showerror("Error", "Failed to delete car")

class CustomersTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Button(self, text="Refresh", command=self.load_customers).pack(anchor="w", padx=5, pady=5)
        
        columns = ("ID", "Username", "Phone")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_customers()

    def load_customers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        customers = storage.get_all_customers()
        for c in customers:
            self.tree.insert("", "end", values=(c.id, c.username, c.phone))

class ShowroomsTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        toolbar = tk.Frame(self)
        toolbar.pack(fill="x", padx=5, pady=5)
        tk.Button(toolbar, text="Refresh", command=self.load_showrooms).pack(side="left", padx=5)
        tk.Button(toolbar, text="Add Showroom", command=self.add_showroom_dialog).pack(side="left", padx=5)
        
        columns = ("ID", "Name", "Location")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_showrooms()

    def load_showrooms(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        showrooms = storage.get_all_showrooms()
        for s in showrooms:
            self.tree.insert("", "end", values=(s.id, s.name, s.location))

    def add_showroom_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Showroom")
        
        tk.Label(dialog, text="Name:").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Location:").pack(pady=5)
        loc_entry = tk.Entry(dialog)
        loc_entry.pack(pady=5)

        tk.Label(dialog, text="Phone:").pack(pady=5)
        phone_entry = tk.Entry(dialog)
        phone_entry.pack(pady=5)
        
        def save():
            name = name_entry.get()
            loc = loc_entry.get()
            phone = phone_entry.get()
            if name and loc and phone:
                sid = storage.next_id_for("showroom")
                showroom = models.Showroom(id=sid, name=name, location=loc, phone=phone, car_ids=[])
                if storage.add_showroom(showroom):
                    storage.push_admin_action(self.controller.current_user.id, "add", "showroom", sid, name)
                    self.load_showrooms()
                    dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields required")
        
        tk.Button(dialog, text="Save", command=save).pack(pady=10)

class GaragesTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        toolbar = tk.Frame(self)
        toolbar.pack(fill="x", padx=5, pady=5)
        tk.Button(toolbar, text="Refresh", command=self.load_garages).pack(side="left", padx=5)
        tk.Button(toolbar, text="Add Garage", command=self.add_garage_dialog).pack(side="left", padx=5)
        
        columns = ("ID", "Name", "Location", "Phone")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_garages()

    def load_garages(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        garages = storage.get_all_garages()
        for g in garages:
            self.tree.insert("", "end", values=(g.id, g.name, g.location, g.phone))

    def add_garage_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Garage")
        
        tk.Label(dialog, text="Name:").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Location:").pack(pady=5)
        loc_entry = tk.Entry(dialog)
        loc_entry.pack(pady=5)

        tk.Label(dialog, text="Phone:").pack(pady=5)
        phone_entry = tk.Entry(dialog)
        phone_entry.pack(pady=5)
        
        def save():
            name = name_entry.get()
            loc = loc_entry.get()
            phone = phone_entry.get()
            if name and loc and phone:
                gid = storage.next_id_for("garage")
                garage = models.Garage(id=gid, name=name, location=loc, phone=phone, service_ids=[])
                if storage.add_garage(garage):
                    storage.push_admin_action(self.controller.current_user.id, "add", "garage", gid, name)
                    self.load_garages()
                    dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields required")
        
        tk.Button(dialog, text="Save", command=save).pack(pady=10)

class ServicesTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        toolbar = tk.Frame(self)
        toolbar.pack(fill="x", padx=5, pady=5)
        tk.Button(toolbar, text="Refresh", command=self.load_services).pack(side="left", padx=5)
        tk.Button(toolbar, text="Add Service", command=self.add_service_dialog).pack(side="left", padx=5)
        
        columns = ("ID", "Name", "Price")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_services()

    def load_services(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        services = storage.get_all_services()
        for s in services:
            self.tree.insert("", "end", values=(s.id, s.name, f"${s.price:,.2f}"))

    def add_service_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Service")
        
        tk.Label(dialog, text="Name:").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Price:").pack(pady=5)
        price_entry = tk.Entry(dialog)
        price_entry.pack(pady=5)
        
        def save():
            try:
                name = name_entry.get()
                price = float(price_entry.get())
                sid = storage.next_id_for("service")
                service = models.Service(id=sid, name=name, price=price)
                if storage.add_service(service):
                    storage.push_admin_action(self.controller.current_user.id, "add", "service", sid, name)
                    self.load_services()
                    dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input")
        
        tk.Button(dialog, text="Save", command=save).pack(pady=10)

class ReservationsTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Button(self, text="Refresh", command=self.load_reservations).pack(anchor="w", padx=5, pady=5)
        
        columns = ("ID", "Customer", "Car", "Start", "Expiry")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_reservations()

    def load_reservations(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        reservations = storage.get_all_reservations()
        for r in reservations:
            customer = storage.get_customer_by_id(r.customer_id)
            car = storage.get_car_by_id(r.car_id)
            cust_name = customer.username if customer else f"ID {r.customer_id}"
            car_name = f"{car.make} {car.model}" if car else f"ID {r.car_id}"
            
            self.tree.insert("", "end", values=(r.reservation_id, cust_name, car_name, r.start_time, r.expiry_time))

class ServiceQueueTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        toolbar = tk.Frame(self)
        toolbar.pack(fill="x", padx=5, pady=5)
        tk.Button(toolbar, text="Refresh", command=self.load_queue).pack(side="left", padx=5)
        tk.Button(toolbar, text="Process Next", command=self.process_next).pack(side="left", padx=5)
        
        columns = ("Req ID", "Customer", "Service", "Garage", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_queue()

    def load_queue(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        queue = storage.service_request_queue
        for req in queue:
            customer = storage.get_customer_by_id(req['customer_id'])
            service = storage.get_service_by_id(req['service_id'])
            garage = storage.get_garage_by_id(req['garage_id'])
            
            cust_name = customer.username if customer else f"ID {req['customer_id']}"
            serv_name = service.name if service else f"ID {req['service_id']}"
            garage_name = garage.name if garage else f"ID {req['garage_id']}"
            
            self.tree.insert("", "end", values=(req['request_id'], cust_name, serv_name, garage_name, req['status']))

    def process_next(self):
        request = storage.dequeue_service_request()
        if request:
            # Create service process
            process_id = storage.next_id_for("service_process")
            service = storage.get_service_by_id(request['service_id'])
            
            service_process = models.ServiceProcess(
                process_id=process_id,
                customer_id=request['customer_id'],
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                amount=service.price if service else 0,
                service_id=request['service_id'],
                garage_id=request['garage_id']
            )
            
            storage.add_service_process(service_process)
            messagebox.showinfo("Success", "Service request processed!")
            self.load_queue()
        else:
            messagebox.showinfo("Info", "Queue is empty")

class StatisticsTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Button(self, text="Refresh", command=self.load_stats).pack(anchor="w", padx=5, pady=5)
        
        self.text = tk.Text(self, font=("Courier", 12))
        self.text.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_stats()

    def load_stats(self):
        self.text.delete(1.0, "end")
        
        cars = storage.get_all_cars()
        customers = storage.get_all_customers()
        showrooms = storage.get_all_showrooms()
        garages = storage.get_all_garages()
        services = storage.get_all_services()
        buy_rent = storage.get_all_buy_rent_processes()
        service_processes = storage.get_all_service_processes()
        reservations = storage.get_all_reservations()
        
        total_buy_rent = sum(p.amount for p in buy_rent)
        total_service = sum(p.amount for p in service_processes)
        
        stats = f"""
SYSTEM STATISTICS
=================

Entities:
  Cars: {len(cars)}
  Customers: {len(customers)}
  Showrooms: {len(showrooms)}
  Garages: {len(garages)}
  Services: {len(services)}

Transactions:
  Buy/Rent Processes: {len(buy_rent)}
  Service Processes: {len(service_processes)}

Queue & Stack:
  Service Request Queue: {storage.get_queue_size()} pending
  Admin Action Stack: {storage.get_stack_size()} actions

Reservations:
  Active Reservations: {len(reservations)}

Revenue:
  Car Sales/Rentals: ${total_buy_rent:,.2f}
  Services: ${total_service:,.2f}
  Total: ${(total_buy_rent + total_service):,.2f}
"""
        self.text.insert("end", stats)

class CustomerDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg="#007bff", height=50)
        header.pack(fill="x")
        tk.Label(header, text=f"Welcome, {controller.current_user.username}", bg="#007bff", fg="white", font=("Helvetica", 12)).pack(side="left", padx=20, pady=10)
        tk.Button(header, text="Logout", command=lambda: controller.show_frame("LoginScreen"), bg="#dc3545", fg="white").pack(side="right", padx=20, pady=10)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.browse_tab = BrowseCarsTab(self.notebook, controller)
        self.notebook.add(self.browse_tab, text="Browse Cars")
        
        self.reservations_tab = MyReservationsTab(self.notebook, controller)
        self.notebook.add(self.reservations_tab, text="My Reservations")

        self.garages_tab = GaragesServicesTab(self.notebook, controller)
        self.notebook.add(self.garages_tab, text="Garages & Services")

        self.requests_tab = ServiceRequestsTab(self.notebook, controller)
        self.notebook.add(self.requests_tab, text="My Service Requests")

        self.history_tab = HistoryTab(self.notebook, controller)
        self.notebook.add(self.history_tab, text="History")

class BrowseCarsTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Search Bar
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(search_frame, text="Make:").pack(side="left", padx=2)
        self.make_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.make_var, width=15).pack(side="left", padx=2)

        tk.Label(search_frame, text="Model:").pack(side="left", padx=2)
        self.model_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.model_var, width=15).pack(side="left", padx=2)
        
        tk.Label(search_frame, text="Max Price:").pack(side="left", padx=2)
        self.price_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.price_var, width=10).pack(side="left", padx=2)
        
        tk.Button(search_frame, text="Search", command=self.search_cars).pack(side="left", padx=10)
        tk.Button(search_frame, text="Reset", command=self.reset_search).pack(side="left")
        
        # Action Buttons
        action_frame = tk.Frame(self)
        action_frame.pack(fill="x", padx=5, pady=5)
        tk.Button(action_frame, text="Buy Selected", command=self.buy_car).pack(side="left", padx=5)
        tk.Button(action_frame, text="Rent Selected", command=self.rent_car).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Make", "Model", "Year", "Price", "Installment")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_cars()

    def load_cars(self, cars=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if cars is None:
            cars = [c for c in storage.get_all_cars() if c.available]
            
        for car in cars:
            inst = "Yes" if car.installment else "No"
            self.tree.insert("", "end", values=(car.id, car.make, car.model, car.year, f"${car.price:,.2f}", inst))

    def search_cars(self):
        filters = {'available': True}
        
        make = self.make_var.get().strip()
        if make:
            filters['make'] = make
            
        model = self.model_var.get().strip()
        if model:
            filters['model'] = model
            
        price = self.price_var.get().strip()
        if price:
            try:
                filters['max_price'] = float(price)
            except ValueError:
                pass
        
        all_cars = storage.get_all_cars()
        filtered = [c for c in all_cars if c.matches_filter(filters)]
        
        self.load_cars(filtered)

    def reset_search(self):
        self.make_var.set("")
        self.model_var.set("")
        self.price_var.set("")
        self.load_cars()

    def buy_car(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        car_id = int(item['values'][0])
        car = storage.get_car_by_id(car_id)
        
        if messagebox.askyesno("Confirm Purchase", f"Buy {car.make} {car.model} for ${car.price:,.2f}?"):
            # Process purchase
            process_id = storage.next_id_for("buy_rent_process")
            process = models.BuyRentProcess(
                process_id=process_id,
                customer_id=self.controller.current_user.id,
                date=datetime.now().strftime("%Y-%m-%d"),
                amount=car.price,
                car_id=car_id,
                type="buy"
            )
            
            if storage.add_buy_rent_process(process):
                car.available = 0
                storage.save_cars()
                messagebox.showinfo("Success", "Car purchased successfully!")
                self.load_cars()
            else:
                messagebox.showerror("Error", "Purchase failed")

    def rent_car(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        car_id = int(item['values'][0])
        car = storage.get_car_by_id(car_id)
        
        # Rent dialog for days
        dialog = tk.Toplevel(self)
        dialog.title("Rent Car")
        
        tk.Label(dialog, text="Days to rent:").pack(pady=5)
        days_entry = tk.Entry(dialog)
        days_entry.pack(pady=5)
        
        def confirm_rent():
            try:
                days = int(days_entry.get())
                rent_price = car.price * 0.01 * days # 1% of price per day assumption
                
                if messagebox.askyesno("Confirm Rent", f"Rent for {days} days? Total: ${rent_price:,.2f}"):
                    process_id = storage.next_id_for("buy_rent_process")
                    process = models.BuyRentProcess(
                        process_id=process_id,
                        customer_id=self.controller.current_user.id,
                        date=datetime.now().strftime("%Y-%m-%d"),
                        amount=rent_price,
                        car_id=car_id,
                        type="rent"
                    )
                    
                    if storage.add_buy_rent_process(process):
                        car.available = 0
                        storage.save_cars()
                        
                        # Add reservation record
                        res_id = storage.next_id_for("reservation")
                        res = models.Reservation(
                            reservation_id=res_id,
                            customer_id=self.controller.current_user.id,
                            car_id=car_id,
                            start_time=datetime.now().strftime("%Y-%m-%d"),
                            expiry_time="TBD"
                        )
                        storage.add_reservation(res)
                        
                        messagebox.showinfo("Success", "Car rented successfully!")
                        self.load_cars()
                        dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid days")

        tk.Button(dialog, text="Confirm", command=confirm_rent).pack(pady=10)

class GaragesServicesTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Split into two panes: Garages list and Services list
        paned = tk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left: Garages
        left_frame = tk.Frame(paned)
        paned.add(left_frame)
        
        tk.Label(left_frame, text="Garages").pack()
        self.garage_tree = ttk.Treeview(left_frame, columns=("ID", "Name"), show="headings")
        self.garage_tree.heading("ID", text="ID")
        self.garage_tree.heading("Name", text="Name")
        self.garage_tree.pack(fill="both", expand=True)
        self.garage_tree.bind("<<TreeviewSelect>>", self.on_garage_select)
        
        # Right: Services
        right_frame = tk.Frame(paned)
        paned.add(right_frame)
        
        tk.Label(right_frame, text="Services in Selected Garage").pack()
        tk.Button(right_frame, text="Book Selected Service", command=self.book_service).pack()
        
        self.service_tree = ttk.Treeview(right_frame, columns=("ID", "Name", "Price"), show="headings")
        self.service_tree.heading("ID", text="ID")
        self.service_tree.heading("Name", text="Name")
        self.service_tree.heading("Price", text="Price")
        self.service_tree.pack(fill="both", expand=True)
        
        self.load_garages()

    def load_garages(self):
        for item in self.garage_tree.get_children():
            self.garage_tree.delete(item)
        for g in storage.get_all_garages():
            self.garage_tree.insert("", "end", values=(g.id, g.name))

    def on_garage_select(self, event):
        selected = self.garage_tree.selection()
        if not selected:
            return
        
        item = self.garage_tree.item(selected[0])
        garage_id = int(item['values'][0])
        
        for item in self.service_tree.get_children():
            self.service_tree.delete(item)
            
        services = storage.get_services_in_garage(garage_id)
        for s in services:
            self.service_tree.insert("", "end", values=(s.id, s.name, f"${s.price:,.2f}"))

    def book_service(self):
        sel_garage = self.garage_tree.selection()
        sel_service = self.service_tree.selection()
        
        if not sel_garage or not sel_service:
            messagebox.showerror("Error", "Select a garage and a service")
            return
            
        garage_id = int(self.garage_tree.item(sel_garage[0])['values'][0])
        service_id = int(self.service_tree.item(sel_service[0])['values'][0])
        
        request_id = storage.enqueue_service_request(self.controller.current_user.id, service_id, garage_id)
        messagebox.showinfo("Success", f"Service booked! Request ID: {request_id}")

class ServiceRequestsTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Button(self, text="Refresh", command=self.load_requests).pack(anchor="w", padx=5, pady=5)
        
        columns = ("Req ID", "Service", "Garage", "Status", "Position")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_requests()

    def load_requests(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        queue = storage.service_request_queue
        my_reqs = [r for r in queue if r['customer_id'] == self.controller.current_user.id]
        
        for req in my_reqs:
            service = storage.get_service_by_id(req['service_id'])
            garage = storage.get_garage_by_id(req['garage_id'])
            position = queue.index(req) + 1
            
            serv_name = service.name if service else f"ID {req['service_id']}"
            garage_name = garage.name if garage else f"ID {req['garage_id']}"
            
            self.tree.insert("", "end", values=(req['request_id'], serv_name, garage_name, req['status'], position))

class HistoryTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Button(self, text="Refresh", command=self.load_history).pack(anchor="w", padx=5, pady=5)
        
        self.text = tk.Text(self, font=("Courier", 10))
        self.text.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_history()

    def load_history(self):
        self.text.delete(1.0, "end")
        cid = self.controller.current_user.id
        
        buy_rent = storage.get_customer_buy_rent_history(cid)
        services = storage.get_customer_service_history(cid)
        
        output = f"Transaction History for {self.controller.current_user.username}\n"
        output += "="*60 + "\n\n"
        
        output += "Car Purchases & Rentals:\n"
        output += "-"*40 + "\n"
        for p in buy_rent:
            car = storage.get_car_by_id(p.car_id)
            car_info = f"{car.make} {car.model}" if car else f"Car {p.car_id}"
            output += f"{p.date} | {p.type.upper()} | {car_info} | ${p.amount:,.2f}\n"
            
        output += "\nServices:\n"
        output += "-"*40 + "\n"
        for p in services:
            service = storage.get_service_by_id(p.service_id)
            serv_name = service.name if service else f"Service {p.service_id}"
            output += f"{p.date} | {serv_name} | ${p.amount:,.2f}\n"
            
        self.text.insert("end", output)

class MyReservationsTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        toolbar = tk.Frame(self)
        toolbar.pack(fill="x", padx=5, pady=5)
        tk.Button(toolbar, text="Refresh", command=self.load_reservations).pack(side="left", padx=5)
        tk.Button(toolbar, text="Cancel Selected", command=self.cancel_reservation).pack(side="left", padx=5)
        
        columns = ("ID", "Car", "Start Date", "Expiry Date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_reservations()

    def load_reservations(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        reservations = storage.get_all_reservations()
        my_res = [r for r in reservations if r.customer_id == self.controller.current_user.id]
        
        for r in my_res:
            car = storage.get_car_by_id(r.car_id)
            car_name = f"{car.make} {car.model}" if car else "Unknown Car"
            self.tree.insert("", "end", values=(r.reservation_id, car_name, r.start_time, r.expiry_time))

    def cancel_reservation(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        res_id = int(item['values'][0])
        
        if messagebox.askyesno("Confirm", f"Cancel reservation ID {res_id}?"):
            if storage.delete_reservation(res_id):
                # Make car available again
                # We need to find which car it was. 
                # Ideally delete_reservation should handle this or we do it manually.
                # In customer_ops.py: 
                # storage.delete_reservation(reservation_id)
                # car = storage.get_car_by_id(reservation.car_id)
                # storage.update_car(car.id, available=1)
                
                # But storage.delete_reservation just removes it from list.
                # We need to get the reservation object first to know the car_id.
                # But we just deleted it? No, we haven't called delete yet.
                
                # Wait, I need to get reservation first.
                res = storage.get_reservation_by_id(res_id)
                if res:
                    storage.delete_reservation(res_id)
                    storage.update_car(res.car_id, available=1)
                    messagebox.showinfo("Success", "Reservation cancelled")
                    self.load_reservations()
                else:
                    messagebox.showerror("Error", "Reservation not found")
            else:
                messagebox.showerror("Error", "Failed to cancel reservation")

if __name__ == "__main__":
    app = CarShowroomApp()
    app.mainloop()
