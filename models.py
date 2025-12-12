# Admin
#   id, username, password
class Admin:
    def __init__(self, id: int, username: str, password: str):
        self.id = int(id)
        self.username = str(username)
        self.password = str(password)

    def check_password(self, password):
        return self.password == password

    def to_csv_row(self):
        return f"{self.id},{self.username},{self.password}"

    @classmethod
    def from_csv_row(cls, row: str):
        parts = row.strip().split(",")
        if len(parts) != 3:
            raise ValueError("Invalid admin CSV row format")

        id = int(parts[0])
        username = parts[1]
        password = parts[2]

        return cls(id, username, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }

    def __repr__(self):
        return f"Admin(id = {self.id} , username = {self.username})"


# Customer
#   id, username, password, phone
class Customer():
    def __init__(self, id: int, username: str, password: str, phone: str):
        self.id = int(id)
        self.username = str(username)
        self.password = str(password)
        self.phone = str(phone)

    def check_password(self, password):
        return self.password == password

    def to_csv_row(self):
        return f"{self.id},{self.username},{self.password},{self.phone}"

    @classmethod
    def from_csv_row(cls, row: str):
        parts = row.strip().split(",")
        if len(parts) != 4:
            raise ValueError("Invalid customer CSV row format")

        id = int(parts[0])
        username = parts[1]
        password = parts[2]
        phone = str(parts[3])

        return cls(id, username, password, phone)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "phone": self.phone
        }

    def __repr__(self):
        return f"customer(id = {self.id} , username = {self.username} , phone = {self.phone})"


# Car
#   id, make, model, year, price, installment, showroom_id, available
class Car:
    def __init__(self, id: int, make: str, model: str, year: int, price: float, installment: int, showroom_id: int,
                 available: int):
        self.id = int(id)
        self.make = str(make)
        self.model = str(model)
        self.year = int(year)
        self.price = float(price)
        self.installment = int(installment)
        self.showroom_id = int(showroom_id)
        self.available = bool(int(available))

    def to_csv_row(self):
        return f"{self.id},{self.make},{self.model},{self.year},{self.price},{self.installment},{self.showroom_id},{1 if self.available else 0}"

    @classmethod
    def from_csv_row(cls, row: str):
        parts = row.strip().split(",")
        if len(parts) != 8:
            raise ValueError("Invalid car CSV row format")

        id = int(parts[0])
        make = parts[1]
        model = parts[2]
        year = int(parts[3])
        price = float(parts[4])
        installment = int(parts[5])
        showroom_id = int(parts[6])
        available = int(parts[7])

        return cls(id, make, model, year, price, installment, showroom_id, available)

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "price": self.price,
            "installment": self.installment,
            "showroom_id": self.showroom_id,
            "available": self.available
        }

    def mark_sold(self):
        self.available = False

    def is_available(self):
        return self.available

    def mark_reserved(self):
        self.available = False

    def mark_available(self):
        self.available = True

    def matches_filter(self, filters: dict):
        if "make" in filters and filters["make"]:
            if filters["make"].lower() not in self.make.lower():
                return False

        if "model" in filters and filters["model"]:
            if filters["model"].lower() not in self.model.lower():
                return False

        if "year" in filters and filters["year"] is not None:
            if self.year != int(filters["year"]):
                return False

        if "min_price" in filters and filters["min_price"] is not None:
            if self.price < float(filters["min_price"]):
                return False

        if "max_price" in filters and filters["max_price"] is not None:
            if self.price > float(filters["max_price"]):
                return False

        if "available" in filters and filters["available"] is not None:
            val = filters["available"]
            if isinstance(val, str):
                val = bool(int(val))  # "1" -> True, "0" -> False
            else:
                val = bool(val)
            if self.available != val:
                return False

        return True

    def update_details(self, make=None, model=None, year=None, price=None, installment=None, showroom_id=None,
                       available=None):
        if make is not None:
            self.make = make

        if model is not None:
            self.model = model

        if year is not None:
            self.year = int(year)

        if price is not None:
            self.price = float(price)

        if installment is not None:
            self.installment = int(installment)

        if showroom_id is not None:
            self.showroom_id = int(showroom_id)

        if available is not None:
            self.available = bool(int(available))

    def __repr__(self):
        return f"id = {self.id}, make = {self.make} , model = {self.model} , year = {self.year} , price = {self.price} ,installment = {self.installment} , showroom_id= {self.showroom_id} , available = {self.available}"


# Showroom
#   id, name, location, phone, car_ids
class Showroom:
    def __init__(self, id: int, name: str, location: str, phone: str, car_ids):
        self.id = int(id)
        self.name = str(name)
        self.location = str(location)
        self.phone = str(phone)
        # قبول list أو string أو None
        # chat gpt (car_ids)
        if isinstance(car_ids, str):
            car_ids = car_ids.strip()
            self.car_ids = [int(x) for x in car_ids.split(";")] if car_ids else []
        else:
            self.car_ids = [int(c) for c in car_ids] if car_ids else []

    @classmethod
    def from_csv_row(cls, row: str):
        parts = row.strip().split(",")
        if len(parts) != 5:
            raise ValueError("Invalid showroom CSV row format")

        id = int(parts[0])
        name = str(parts[1])
        location = str(parts[2])
        phone = str(parts[3])
        if parts[4].strip() == "":
            car_ids = []
        else:
            car_ids = [int(x) for x in parts[4].split(";")]
        return cls(id, name, location, phone, car_ids)

    def to_csv_row(self):
        car_ids_str = ";".join(str(x) for x in self.car_ids)
        return f"{self.id},{self.name},{self.location},{self.phone},{car_ids_str}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "phone": self.phone,
            "car_ids": self.car_ids,
        }

    def __repr__(self):
        return f"Showroom (id = {self.id}, name = {self.name} , location = {self.location} , phone = {self.phone} , car_ids = {self.car_ids} )"

    def add_car(self, car_id: int) -> bool:
        car_id = int(car_id)
        if car_id in self.car_ids:
            return False
        self.car_ids.append(car_id)
        return True

    def remove_car(self, car_id: int) -> bool:
        car_id = int(car_id)
        if car_id in self.car_ids:
            self.car_ids.remove(car_id)
            return True
        return False

    def update_details(self, name=None, location=None, phone=None):
        if name is not None:
            self.name = name

        if location is not None:
            self.location = location

        if phone is not None:
            self.phone = phone

    def get_car_ids(self):
        return list(self.car_ids)

    def has_car(self, car_id: int) -> bool:
        return int(car_id) in self.car_ids

    def matches_filter(self, filters: dict):
        name = filters.get("name")
        location = filters.get("location")

        if name and name.lower() not in self.name.lower():
            return False

        if location and location.lower() not in self.location.lower():
            return False

        return True

# Garage
#   id, name, location, phone, service_ids
class Garage:
    def __init__(self, id: int, name: str, location: str, phone: str, service_ids):
        self.id = int(id)
        self.name = str(name)
        self.location = str(location)
        self.phone = str(phone)
        if isinstance(service_ids, str):
            service_ids = service_ids.strip()
            self.service_ids = [int(x) for x in service_ids.split(";")] if service_ids else []
        else:
            self.service_ids = [int(c) for c in service_ids] if service_ids else []

    @classmethod
    def from_csv_row(cls, row: str):
        parts = row.strip().split(",")
        if len(parts) != 5:
            raise ValueError("Invalid garage CSV row format")

        id = int(parts[0])
        name = str(parts[1])
        location = str(parts[2])
        phone = str(parts[3])
        if parts[4].strip() == "":
            service_ids = []
        else:
            service_ids = [int(x) for x in parts[4].split(";")]
        return cls(id, name, location, phone, service_ids)

    def to_csv_row(self):
        service_ids_str = ";".join(str(x) for x in self.service_ids)
        return f"{self.id},{self.name},{self.location},{self.phone},{service_ids_str}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "phone": self.phone,
            "service_ids": self.service_ids,
        }

    def __repr__(self):
        return f"Garage (id = {self.id}, name = {self.name} , location = {self.location} , phone = {self.phone} , service_ids = {self.service_ids} )"

    def add_service(self, service_id: int) -> bool:
        service_id = int(service_id)
        if service_id in self.service_ids:
            return False
        self.service_ids.append(service_id)
        return True

    def remove_service(self, service_id: int) -> bool:
        service_id = int(service_id)
        if service_id in self.service_ids:
            self.service_ids.remove(service_id)
            return True
        return False

    def update_details(self, name=None, location=None, phone=None):
        if name is not None:
            self.name = name

        if location is not None:
            self.location = location

        if phone is not None:
            self.phone = phone

    def get_service_ids(self):
        return list(self.service_ids)

    def matches_filter(self, filters: dict):
        name = filters.get("name")
        location = filters.get("location")

        if name and name.lower() not in self.name.lower():
            return False

        if location and location.lower() not in self.location.lower():
            return False

        return True


# Service
#   id, name, price
class Service:
    def __init__(self, id: int, name: str, price: float):
        self.id = int(id)
        self.name = str(name)
        self.price = float(price)

    def to_csv_row(self):
        return f"{self.id},{self.name},{self.price}"

    @classmethod
    def from_csv_row(cls, row: str):
        parts = row.strip().split(",")
        if len(parts) != 3:
            raise ValueError("Invalid Service CSV row format")

        id = int(parts[0])
        name = parts[1]
        price = float(parts[2])

        return cls(id, name, price)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,

        }

    def __repr__(self):
        return f"Service (id = {self.id}, name = {self.name} , price = {self.price} )"

    def update_details(self, name=None, price=None):
        if name is not None:
            self.name = name

        if price is not None:
            self.price = float(price)

    def price_display(self):
        return f"{self.price} EGP"

    def matches_filter(self, filters: dict):
        name = filters.get("name")
        if name and name.lower() not in self.name.lower():
            return False
        return True


# BuyRentProcess
#   process_id, customer_id, date, amount, car_id, type
class BuyRentProcess:
    def __init__(self, process_id: int, customer_id: int, date: str, amount: float, car_id: int, type: str):
        self.process_id = int(process_id)
        self.customer_id = int(customer_id)
        self.date = str(date)
        self.amount = float(amount)
        self.car_id = int(car_id)
        self.type = str(type)

    def to_csv_row(self):
        return f"{self.process_id},{self.customer_id},{self.date},{self.amount},{self.car_id},{self.type}"

    @classmethod
    def from_csv_row(cls, row: str):
        parts = row.strip().split(",")
        if len(parts) != 6:
            raise ValueError("Invalid BuyRentProcess CSV row format")

        process_id = int(parts[0])
        customer_id = int(parts[1])
        date = str(parts[2])
        amount = float(parts[3])
        car_id = int(parts[4])
        type = str(parts[5])

        return cls(process_id, customer_id, date, amount, car_id, type)

    def to_dict(self):
        return {
            "process_id": self.process_id,
            "customer_id": self.customer_id,
            "date": self.date,
            "amount": self.amount,
            "car_id": self.car_id,
            "type": self.type,
        }

    def __repr__(self):
        return f"BuyRentProcess (process_id = {self.process_id}, customer_id = {self.customer_id} , date = {self.date},amount = {self.amount}, car_id = {self.car_id} , type = {self.type} )"

    def is_rent(self):
        return self.type.lower() == "rent"

    def is_buy(self):
        return self.type.lower() == "buy"


# ServiceProcess
#   process_id, customer_id, date, amount, service_id, garage_id
class ServiceProcess:
    def __init__(self, process_id: int, customer_id: int, date: str, amount: float, service_id: int, garage_id: int):
        self.process_id = int(process_id)
        self.customer_id = int(customer_id)
        self.date = str(date)
        self.amount = float(amount)
        self.service_id = int(service_id)
        self.garage_id = int(garage_id)

    def to_csv_row(self):
        return f"{self.process_id},{self.customer_id},{self.date},{self.amount},{self.service_id},{self.garage_id}"

    @classmethod
    def from_csv_row(cls, row: str):
        parts = row.strip().split(",")
        if len(parts) != 6:
            raise ValueError("Invalid ServiceProcess CSV row format")

        process_id = int(parts[0])
        customer_id = int(parts[1])
        date = str(parts[2])
        amount = float(parts[3])
        service_id = int(parts[4])
        garage_id = int(parts[5])

        return cls(process_id, customer_id, date, amount, service_id, garage_id)

    def to_dict(self):
        return {
            "process_id": self.process_id,
            "customer_id": self.customer_id,
            "date": self.date,
            "amount": self.amount,
            "service_id": self.service_id,
            "garage_id": self.garage_id,
        }

    def __repr__(self):
        return f"ServiceProcess (process_id = {self.process_id}, customer_id = {self.customer_id} , date = {self.date},amount = {self.amount}, service_id = {self.service_id} , garage_id = {self.garage_id} )"

    def get_service_name(self, services_by_id):
        service = services_by_id.get(self.service_id)
        return service.name if service else "Unknown Service"


# Reservation
#   reservation_id, customer_id, car_id, start_time, expiry_time
class Reservation:
    def __init__(self, reservation_id: int, customer_id: int, car_id: int, start_time: str, expiry_time: str):
        self.reservation_id = int(reservation_id)
        self.customer_id = int(customer_id)
        self.car_id = int(car_id)
        self.start_time = str(start_time)
        self.expiry_time = str(expiry_time)

    def to_csv_row(self):
        return f"{self.reservation_id},{self.customer_id},{self.car_id},{self.start_time},{self.expiry_time}"

    @classmethod
    def from_csv_row(cls, row: str):
        parts = row.strip().split(",")
        if len(parts) != 5:
            raise ValueError("Invalid Reservation CSV row format")

        reservation_id = int(parts[0])
        customer_id = int(parts[1])
        car_id = int(parts[2])
        start_time = str(parts[3])
        expiry_time = str(parts[4])

        return cls(reservation_id, customer_id, car_id, start_time, expiry_time)

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "car_id": self.car_id,
            "start_time": self.start_time,
            "expiry_time": self.expiry_time,
        }

    def __repr__(self):
        return f"Reservation (reservation_id = {self.reservation_id}, customer_id = {self.customer_id} , car_id = {self.car_id}, start_time = {self.start_time} , expiry_time = {self.expiry_time} )"
