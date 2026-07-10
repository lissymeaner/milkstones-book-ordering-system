"""Example model objects that can be used during testing of the program."""

# modules
import bookstore__customer, bookstore__order, bookstore__product
from bookstore__customer import Customer
from bookstore__order import Order
from bookstore__product import BookOrderItem

# To show up in the 'Search Orders' treeview
example_order_customer = Customer(0, "Jane Bloggs", "jane.bloggs@example.com", "0800 000 0000")

# <BookOrderItem>s
boi_for_order1 = BookOrderItem(0, 6, True, 7.99, "9781250823946", 2001, "Story of My Life", "Joe Bloggs", 326, "Biography", 1, (7.99 * 1)) # NEVER HARD CODE THE AMOUNT, USE THE <unit_price> * <quantity> FORMULA
boi_for_order2 = BookOrderItem(1, 7, True, 13.99, "9781250125835", 2026, "Hell Girls Are Back", "Joey Bloggs", 449, "Fantasy", 4, (13.99 * 4))
boi_for_order3 = BookOrderItem(2, 2, True, 4.99, "9781250852380", 1975, "Hotel 501", "Ness", 271, "Romance", 1, (4.99 * 1))
boi_for_order4 = BookOrderItem(3, 150, True, 10.49, "9780241137291", 2037, "Bear, What Do You Smell?", "Erika Carlie", 12, "Children's", 30, (10.49 * 30))

# Experiments with adding subtotals of <BookOrderItem>s
example_subtotal = boi_for_order1+boi_for_order2
example_subtotal2 = boi_for_order3+boi_for_order4
EXAMPLE_SHIPPING = 3.99

# Lists of <BookOrderItem>s
example_order_bois = [boi_for_order1, boi_for_order2]
example_order_bois2 = [boi_for_order3, boi_for_order4]

# <Order>s and list of <Order>s
example_order = Order(0, example_order_bois, example_order_customer, example_subtotal, EXAMPLE_SHIPPING, example_subtotal + EXAMPLE_SHIPPING, "")
example_order2 = Order(1, example_order_bois2, example_order_customer, example_subtotal2, 0.00, example_subtotal2 + 0.00, "")
example_orders = [example_order, example_order2]