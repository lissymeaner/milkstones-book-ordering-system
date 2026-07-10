###################################################################################################################
# region ############################################ MODULES #####################################################
###################################################################################################################
from bookstore__product import Book, BookOrderItem
from bookstore__order import Order, OrderDetails
from bookstore__customer import Customer
from typing import List
import pickle
from pathlib import Path
import re
# import bookstore_models
# endregion
###################################################################################################################

###################################################################################################################
# region ########################################### VARIABLES ####################################################
###################################################################################################################

############################################# Arrays to add objects to ############################################
###################################################################################################################
books: List[Book] = [] # A list of books to stock and store onto the system.
book_titles: List[str] = [] # A list of book titles, useful for less complicated lookups.
book_order_items: List[BookOrderItem] = [] # A list of book items to ship for a single order.
customers: List[Customer] = [] # A list of Milkstones customers to store onto the system.
orders: List[Order] = [] # A list of orders onto the system.

# endregion
###################################################################################################################

###################################################################################################################
# region ########################################### CONSTANTS ####################################################
###################################################################################################################

B_FILE = r'`pickle\books.pkl'
C_FILE = r'`pickle\customers.pkl'
O_FILE = r'`pickle\orders.pkl'

# endregion
###################################################################################################################

###################################################################################################################
# region ########################################### FUNCTIONS ####################################################
###################################################################################################################

def load_pickle(file_name):
  '''Loads every object from a pickle file of your choice and returns a list of objects.
  E.g. this function will return an entire list of books, available or not.'''
  # Checking if the chosen pickle file does exist.
  # If the file does exist, then open and read it.
  if Path(file_name).exists():
    with open(file_name, 'rb') as f:
      try:
        return pickle.load(f) # Try returning an objects list,
                    # if any objects have been appended to the file.
      except:
        return [] # Otherwise, return an empty list.
  else:
    return [] # If the pickle file does not exist, return an empty list.

def update_pickle(file_name, objs):
  '''Updates a Pickle file with a list of objects.'''
  with open(file_name, 'wb') as f:
    pickle.dump(objs, file=f)

def add_book(stock, in_stock, unit_price, isbn, year, title,
       author, pages, genre):
  '''Adds a Book object to the books.pkl file.'''
  ################################################## VARIABLES ##################################################
  global books, book_titles
  
  # 2. Initialise book_id
  try:
    book_id = int(books[len(books) - 1].id) + 1
  except:
    book_id = 0
  
  # 3. Convert the unit price of the book to 2 decimal points,
  #  as this is currency.
  unit_price = f'{float(unit_price):.2f}'
  
  # 4. Cast numbers from numeric string arguments
  stock = int(stock)
  unit_price = float(unit_price)
  year = int(year)
  pages = int(pages)
  
  ################################################### PROCESS ###################################################
  # 5. Create a <Book> instance called <book>
  book = Book(book_id, stock, in_stock, unit_price, isbn, year, title, author, pages, genre)
  
  books.append(book) # 6. Add book to the list
  book_titles.append(book.name) # 7. Add book title to the list of book titles
  
  save_books() # 8. Save the updated <books> list into 'books.pkl'
  
  # print(f'Book added successfully to "{B_FILE[8:]}".') <--- USE THIS MESSAGE FOR DEBUGGING
  
  return book # 9. Return the book for re-use with any file.

def add_customer(email, phone, name):
  '''Adds a Customer object to the customers.pkl file.'''
  ################################################## VARIABLES ##################################################
  global customers
  
  # 2. Initialise customer_id
  try:
    customer_id = int(customers[len(customers) - 1].id) + 1
  except:
    customer_id = 0
  
  ################################################### PROCESS ###################################################
  # 3. Create a <Customer> instance called <customer>
  customer = Customer(customer_id, email, phone, name)
  
  # 4. Check if the customer's phone is a national phone number,
  #  it doesn't matter which country it is from.
  customer.phone = customer.format_phone() 
  
  customers.append(customer) # 5. Add customer to the list
  
  save_customers() # 6. Save the updated <customers> list into 'customers.pkl'
  
  # print(f'Customer added successfully to "{C_FILE[8:]}".') <--- USE THIS MESSAGE FOR DEBUGGING
  
  return customer # 7. Return the customer for re-use with any file

def add_order(order_items, total, shipping, customer, sub_total):
  '''Adds an Order object to the orders.pkl file.'''
  ################################################## VARIABLES ##################################################
  global orders
  
  # 2. Initialise order_id by using the expression of...
  #  (new order ID = (the ID of the last order in the <orders> list) + 1)
  try:
    order_id = int(orders[len(orders) - 1].id) + 1
  except: # In the case where there are no elements in <orders>,
    order_id = 0 # this number ID will represent the first order to append to.
  
  ################################################### PROCESS ###################################################
  # 3. Create a new instance of OrderDetails called <od>, to prepare the new Order object
  od = OrderDetails(order_items, total, shipping, customer, sub_total)
  
  # 4. Create an Order object with some of the details from the <od> OrderDetails object, d
  order = Order(order_id, od.order_items, od.total, od.shipping,
          od.generate_invoice_path(), od.customer, od.sub_total)
  
  orders.append(order) # 5. Add order to the list
  
  save_orders() # 6. Save the order into 'orders.pkl'
  
  # print(f'Order added successfully to "{O_FILE[8:]}".') <--- USE THIS MESSAGE FOR DEBUGGING
  
  return order # 7. Return the order for re-use with any file.

## Procedures for saving books, customers and orders. ##
def save_books():
  '''Saves books to books.pkl.'''
  update_pickle(B_FILE, books)

def save_customers():
  '''Saves customers to customers.pkl.'''
  update_pickle(C_FILE, customers)

def save_orders():
  '''Saves orders to orders.pkl.'''
  update_pickle(O_FILE, orders)

############################################## VALIDATION FUNCTIONS ###############################################
def validate_as_int(*values):
  """Validates any value as an integer."""
  if len(values) > 0:
    result = [] # All arguments go here
    for value in values:
      try:
        result.append(int(value))
      except ValueError: # If any one argument cannot be an integer, ... just return False
        return False
    return True # ...because all arguments need to be integers to return True
  elif len(values) == 0:
    result = values[0] # In the case that there is only one argument
    try:
      int(result)
      return True
    except ValueError:
      return False
  else:
    return False
  
def validate_as_float(*values):
  """Validates any value as a float."""
  # See comments from validate_as_int(*values)
  if len(values) > 0:
    result = []
    for value in values:
      try:
        result.append((float(value)))
      except ValueError:
        return False
    return True
  elif len(values) == 0:
    result = values[0]
    try:
      float(result)
      return True
    except ValueError:
      return False
  else:
    return False
  
def validate_as_string(*values):
  """Validates any value as a string."""
  # See comments from validate_as_int(*values)
  if len(values) > 0:
    result = []
    for value in values:
      try:
        result.append(str(value))
      except ValueError:
        return False
    return True
  elif len(values) == 0:
    result = values[0]
    try:
      return True
    except ValueError:
      return False
  else:
    return False

def validate_as_email(email):
  """Validates any value as an email string."""
  # See comments from validate_as_int(*values)
  
  # Formatting for email -> (jane_doe@example.com)
  regex = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}'
  
  if re.fullmatch(regex, email):
    return True
  else:
    return False

def search_order(query):
  ################################################## VARIABLES ##################################################
  global orders
  ###############################################################################################################
  
  if validate_as_int(query): # If the query can be an integer,
    query = int(query) # ... convert the query into an integer.
    
    # This process uses linear search. O(N), avg. case scenario
    for order in orders:
      if query != order.id:
        pass # Keep searching if query does not match
      else:
        return order # Otherwise, return order.
    return None

def compare_quantity_and_stock(quantity, stock):
  '''Compares chosen quantity of an order item against the stock of the product being added to the cart.
  Parameters:
    quantity (int): The quantity of an order item *for* a product
    stock (int): The stock of a product
  Returns:
    bool: Boolean value for whether quantity is less than stock.
  '''
  if validate_as_int(quantity, stock):
    if quantity > stock:
      return False
    else:
      return True
  else:
    return False

# endregion
###################################################################################################################

###################################################################################################################
# region ######################################### INITIALISATION #################################################
###################################################################################################################

# Populate lists by loading saved Pickle file objects
books = load_pickle(B_FILE) # Loads existing books from 'books.pkl'
customers = load_pickle(C_FILE) # Loads existing customers from 'customers.pkl'
orders = load_pickle(O_FILE) # Loads existing orders from 'orders.pkl'

# Append book_titles with titles of books (string).
for book in books:
  book_titles.append(f'{book.name}')

# endregion
###################################################################################################################

###################################################################################################################
# region ############################################# DEBUG ######################################################
###################################################################################################################
# print(compare_quantity_and_stock(3, 9)) # Outputs True
# print(compare_quantity_and_stock(9, 3)) # Outputs False
# print(compare_quantity_and_stock(9, 3, 1)) # Do not use at all

# endregion
###################################################################################################################