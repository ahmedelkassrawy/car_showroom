from models import Car, Showroom, Garage, Service

def search_cars(cars_list, filters):
    filtered_cars = []
    for car in cars_list:
        if car.matches_filter(filters):
            filtered_cars.append(car)
    return filtered_cars

def search_showrooms(showrooms_list, filters):
    filtered_showrooms = []
    for showroom in showrooms_list:
        if showroom.matches_filter(filters):
            filtered_showrooms.append(showroom)
    return filtered_showrooms

def search_garages(garages_list, filters):
    filtered_garages = []
    for garage in garages_list:
        if garage.matches_filter(filters):
            filtered_garages.append(garage)
    return filtered_garages

def search_services(services_list, name=None):
    return [s for s in services_list if s.matches_filter(name)]

def search_cars_in_showroom(showroom, all_cars, filters):
    cars_in_showroom = []
    for car in all_cars :
        if car.id in showroom.car_ids:
            if car.matches_filter(filters):
                cars_in_showroom.append(car)
    return cars_in_showroom

def general_car_search(filters):
    """General car search across all cars with filters."""
    import storage
    all_cars = storage.get_all_cars()
    
    # If available_only flag is set, only return available cars
    if filters.get('available_only'):
        all_cars = [car for car in all_cars if car.available]
        # Remove the flag from filters before passing to matches_filter
        filters = {k: v for k, v in filters.items() if k != 'available_only'}
    
    return search_cars(all_cars, filters)