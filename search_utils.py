# ================================
# search_utils.py
# Contains all search functions used by admin_ops and customer_ops
# ================================
from models import Car, Showroom, Garage, Service

# --------------------------------
# search_cars(cars_list, filters)
# - Output: list of Car objects that match the filters
# --------------------------------
def search_cars(cars_list, filters):
    filtered_cars = []
    for car in cars_list:
        if car.matches_filter(filters):
            filtered_cars.append(car)
    return filtered_cars

# --------------------------------
# search_showrooms(showrooms_list, name=None, location=None)
# - Output: list of Showroom objects
# --------------------------------
def search_showrooms(showrooms_list, filters):
    filtered_showrooms = []
    for showroom in showrooms_list:
        if showroom.matches_filter(filters):
            filtered_showrooms.append(showroom)
    return filtered_showrooms
# --------------------------------
# search_garages(garages_list, name=None, location=None)
# - Output: list of Garage objects
# --------------------------------
def search_garages(garages_list, filters):
    filtered_garages = []
    for garage in garages_list:
        if garage.matches_filter(filters):
            filtered_garages.append(garage)
    return filtered_garages
# --------------------------------
# search_services(services_list, name=None)
# - Output: list of Service objects
# --------------------------------
def search_services(services_list, name=None):
    return [s for s in services_list if s.matches_filter(name)]


# --------------------------------
# search_cars_in_showroom(showroom, all_cars, filters)
# - Gets cars that belong only to this showroom
# --------------------------------
def search_cars_in_showroom(showroom, all_cars, filters):
    cars_in_showroom = []
    for car in all_cars :
        if car.id in showroom.car_ids:
            if car.matches_filter(filters):
                cars_in_showroom.append(car)
    return cars_in_showroom