# Data Structures Documentation

This document explains all data structures used in the Car Showroom Management System and their purposes.

## Overview

The project uses various data structures optimized for different operations:
- **Dictionaries (Hash Maps)** for fast lookups by ID
- **Lists** for maintaining history and chronological records
- **Queue (FIFO)** for service request management
- **Stack (LIFO)** for admin action history and undo functionality

---

## 1. Dictionaries (Hash Maps)

### Location: `storage.py` (lines 24-29)

```python
cars_by_id = {}
customers_by_id = {}
showrooms_by_id = {}
garages_by_id = {}
services_by_id = {}
reservations_by_id = {}
```

### Purpose
Dictionaries provide **O(1)** average-case time complexity for lookups, insertions, and deletions by ID.

### Usage

#### `cars_by_id`
- **Key**: Car ID (integer)
- **Value**: Car object
- **Use Case**: Quick retrieval of car information by ID when displaying details, updating availability, or processing transactions
- **Functions**: `get_car_by_id()`, `add_car()`, `update_car()`, `delete_car()`

#### `customers_by_id`
- **Key**: Customer ID (integer)
- **Value**: Customer object
- **Use Case**: Fast customer authentication and profile management
- **Functions**: `get_customer_by_id()`, `add_customer()`, `update_customer()`, `delete_customer()`

#### `showrooms_by_id`
- **Key**: Showroom ID (integer)
- **Value**: Showroom object
- **Use Case**: Retrieve showroom details and associated cars
- **Functions**: `get_showroom_by_id()`, `add_showroom()`, `update_showroom()`, `delete_showroom()`

#### `garages_by_id`
- **Key**: Garage ID (integer)
- **Value**: Garage object
- **Use Case**: Manage garage information and available services
- **Functions**: `get_garage_by_id()`, `add_garage()`, `update_garage()`, `delete_garage()`

#### `services_by_id`
- **Key**: Service ID (integer)
- **Value**: Service object
- **Use Case**: Quick service lookup for pricing and availability
- **Functions**: `get_service_by_id()`, `add_service()`, `update_service()`, `delete_service()`

#### `reservations_by_id`
- **Key**: Reservation ID (integer)
- **Value**: Reservation object
- **Use Case**: Manage temporary car reservations with expiration times
- **Functions**: `get_reservation_by_id()`, `add_reservation()`, `delete_reservation()`

---

## 2. Lists (Arrays)

### Location: `storage.py` (lines 31-32)

```python
buy_rent_history = []
service_history = []
```

### Purpose
Lists maintain chronological order and allow iteration over historical records. They provide **O(1)** append operations and **O(n)** search operations.

### Usage

#### `buy_rent_history`
- **Type**: List of BuyRentProcess objects
- **Order**: Chronological (insertion order)
- **Use Case**: 
  - Track all car purchase and rental transactions
  - Generate customer transaction history
  - Calculate total revenue
  - Filter by customer or date
- **Functions**: `add_buy_rent_process()`, `get_customer_buy_rent_history()`, `get_all_buy_rent_processes()`

#### `service_history`
- **Type**: List of ServiceProcess objects
- **Order**: Chronological (insertion order)
- **Use Case**: 
  - Record all service bookings
  - View customer service history
  - Track garage revenue
  - Service analytics
- **Functions**: `add_service_process()`, `get_customer_service_history()`, `get_all_service_processes()`

---

## 3. Queue (FIFO - First In, First Out)

### Location: `storage.py` (line 35)

```python
service_request_queue = []
```

### Purpose
Implements **FIFO** behavior for fair service request processing. First customer to request gets served first.

### Structure
Each element is a dictionary containing:
```python
{
    'request_id': int,
    'customer_id': int,
    'service_id': int,
    'garage_id': int,
    'timestamp': string (datetime),
    'status': string ('pending', 'processing', 'completed')
}
```

### Queue Operations

#### Enqueue (Add to Queue)
- **Function**: `enqueue_service_request(customer_id, service_id, garage_id)`
- **Operation**: Append to end of list
- **Time Complexity**: O(1)
- **Use Case**: Customer requests a service

#### Dequeue (Remove from Queue)
- **Function**: `dequeue_service_request()`
- **Operation**: Remove from front of list (index 0)
- **Time Complexity**: O(n) - due to list shifting
- **Use Case**: Admin/garage processes the next service request

#### Peek (View First)
- **Function**: `peek_service_request_queue()`
- **Operation**: View first element without removal
- **Time Complexity**: O(1)
- **Use Case**: Check which request is next

#### View Queue
- **Function**: `view_service_request_queue()`
- **Operation**: Display all requests in order
- **Use Case**: Admin views all pending service requests

### Workflow Example
```
Customer 1 requests oil change    → [Request 1]
Customer 2 requests tire rotation → [Request 1, Request 2]
Customer 3 requests brake check   → [Request 1, Request 2, Request 3]
Process next request              → [Request 2, Request 3]  (Request 1 completed)
```

---

## 4. Stack (LIFO - Last In, First Out)

### Location: `storage.py` (line 38)

```python
admin_action_stack = []
```

### Purpose
Implements **LIFO** behavior for undo functionality. Most recent action is undone first.

### Structure
Each element is a dictionary containing:
```python
{
    'action_id': int,
    'admin_id': int,
    'action_type': string ('add', 'update', 'delete'),
    'entity_type': string ('car', 'customer', 'showroom', 'garage', 'service'),
    'entity_id': int,
    'timestamp': string (datetime),
    'details': string (optional - stores state for undo)
}
```

### Stack Operations

#### Push (Add to Stack)
- **Function**: `push_admin_action(admin_id, action_type, entity_type, entity_id, details)`
- **Operation**: Append to end of list
- **Time Complexity**: O(1)
- **Use Case**: Record every admin action for potential undo

#### Pop (Remove from Stack)
- **Function**: `pop_admin_action()`
- **Operation**: Remove from end of list (last element)
- **Time Complexity**: O(1)
- **Use Case**: Undo the most recent admin action

#### Peek (View Top)
- **Function**: `peek_admin_action_stack()`
- **Operation**: View last element without removal
- **Time Complexity**: O(1)
- **Use Case**: Check what action would be undone

#### View Stack
- **Function**: `view_admin_action_stack(limit=10)`
- **Operation**: Display recent actions (most recent first)
- **Use Case**: Admin reviews recent actions

#### Clear Stack
- **Function**: `clear_admin_action_stack()`
- **Operation**: Remove all actions
- **Use Case**: Clear action history

### Workflow Example
```
Admin adds Car 1          → [Action 1: Add Car 1]
Admin updates Showroom 2  → [Action 1, Action 2: Update Showroom 2]
Admin deletes Service 3   → [Action 1, Action 2, Action 3: Delete Service 3]
Undo last action          → [Action 1, Action 2]  (Service 3 restored)
Undo last action          → [Action 1]  (Showroom 2 changes reverted)
```

---

## Data Persistence

All data structures are persisted to CSV files in the `data/` directory:

| Data Structure | CSV File | Persistence |
|----------------|----------|-------------|
| `cars_by_id` | `cars.csv` | Yes |
| `customers_by_id` | `customers.csv` | Yes |
| `showrooms_by_id` | `showrooms.csv` | Yes |
| `garages_by_id` | `garages.csv` | Yes |
| `services_by_id` | `services.csv` | Yes |
| `reservations_by_id` | `reservations.csv` | Yes |
| `buy_rent_history` | `buy_rent_process.csv` | Yes |
| `service_history` | `service_process.csv` | Yes |
| `service_request_queue` | `service_request_queue.csv` | Yes |
| `admin_action_stack` | `admin_action_stack.csv` | Yes |

### Load/Save Functions
- **Load**: `load_all_data()` - Called at program startup
- **Save**: `save_all_data()` - Called before program exit
- **Auto-save**: Individual save functions called after modifications

---

## Time Complexity Summary

| Operation | Data Structure | Time Complexity |
|-----------|----------------|-----------------|
| Lookup by ID | Dictionary | O(1) average |
| Add entity | Dictionary | O(1) average |
| Update entity | Dictionary | O(1) average |
| Delete entity | Dictionary | O(1) average |
| Add to history | List (append) | O(1) |
| Search history | List (linear search) | O(n) |
| Enqueue | Queue (list append) | O(1) |
| Dequeue | Queue (list pop front) | O(n) |
| Push | Stack (list append) | O(1) |
| Pop | Stack (list pop end) | O(1) |

---

## Design Decisions

### Why Dictionaries for Entities?
- Fast lookups by ID are critical for user operations
- Most operations (view details, update, delete) require ID-based access
- Memory overhead is acceptable for the scale of this application

### Why Lists for History?
- Natural chronological ordering
- Simple iteration for filtering and reporting
- Append-only operations are fast

### Why Queue for Service Requests?
- Ensures fairness (first-come, first-served)
- Clear business logic for service processing
- Easy to visualize customer wait position

### Why Stack for Admin Actions?
- Natural undo behavior (reverse chronological)
- LIFO matches user expectations for undo
- Simple to implement and understand

---

## Future Optimizations

### For Large-Scale Deployment:
1. **Priority Queue** - Add priority levels for VIP customers
2. **Indexed Database** - Replace CSV with SQLite for complex queries
3. **Deque** - Use `collections.deque` for O(1) dequeue operations
4. **LRU Cache** - Cache frequently accessed entities
5. **Binary Search Tree** - For sorted data and range queries

---

## Module Organization

```
car_showroom/
├── storage.py           # Data structures and CRUD operations
├── models.py            # Entity classes (Car, Customer, etc.)
├── customer_ops.py      # Customer operations
├── admin_ops.py         # Admin operations
├── search_utils.py      # Search and filter functions
├── main.py              # Application entry point
└── data/                # CSV files (persistent storage)
    ├── cars.csv
    ├── customers.csv
    ├── showrooms.csv
    ├── garages.csv
    ├── services.csv
    ├── buy_rent_process.csv
    ├── service_process.csv
    ├── reservations.csv
    ├── service_request_queue.csv
    └── admin_action_stack.csv
```

---

## Contributing

When adding new data structures:
1. Choose the appropriate structure based on access patterns
2. Document time complexity for main operations
3. Add persistence if data should survive restarts
4. Update this documentation
