"""The graphical user interface (GUI) for the Milkstones online bookstore system."""
###################################################################################################################
# region ############################################ Modules #####################################################
###################################################################################################################
import tkinter as tk
from tkinter import ttk, messagebox as mb
import bookstore_core as core
from bookstore__product import Book, BookOrderItem
from bookstore__order import Order
import bookstore_models as bm
# endregion
###################################################################################################################

###################################################################################################################
# region ############################################ Classes #####################################################
###################################################################################################################
class DFrame(tk.Frame): # Stands for 'Debug frame', which debugs a frame by setting different bg colour from another frame
    """
    Extension of tk.Frame with an optional debug mode, which randomises the colour within greyscale, for easy debugging frame structure.
    """
    DEBUG_MODE = True
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        if DFrame.DEBUG_MODE:
            self.config(background="#" + (self.__randhex() + self.__randhex()) * 3)
        
    def __randhex(self) -> str:
        """
        Returns a random hex digit between A and F.
        """
        import random
        def nprc(lst):
            return random.choice(lst)
        return nprc(list("ABCDEF"))

class DDFrame (ttk.Frame): # Use this class for children of DFrames, e.g. this will debug a tab by setting different borderwidth (padding of entire tab) from another tab
    """
    Extension of ttk.Frame, adapting features from the DFrame subclass
    """
    DEBUG_MODE = True
    def __init__(self, master=None, **kw):
      super().__init__(master, **kw)
      if ttk.Frame.DEBUG_MODE:
          import random as rand
          self.config(borderwidth=rand.randint(50,100))
# endregion
###################################################################################################################

###################################################################################################################
# region ########################################### Constants ####################################################
###################################################################################################################

REQUIRED_MSG = "All fields are required." # Generic message at the end of all add frames,
                                          # forces the user to enter all fields for their new book /
                                          # customer.
ADDED_TO_SYS_MSG = "has been successfully added to our system." # Generic message for adding book / customer objects.
SUCCESS_MSG = "Your order has been placed successfully." # Success message

URGENT_SHIPPING_COST = 3.99
FREE_SHIPPING_COST = 0
# endregion
###################################################################################################################

###################################################################################################################
# region ########################################### Functions ####################################################
###################################################################################################################

def make_treeview(frame, columns):
    '''Alias for ttk.Treeview, which constructs a treeview.'''
    new_treeview = ttk.Treeview(frame, columns=columns, show="headings")
    return new_treeview # return the new Treeview

def make_treeview_heading(treeview, columns, columns_display, columns_width):
    '''Constructs treeview headings for all user-set columns.
    Useful for treeviews with a large number of columns.'''
    # Runs for each string in the <column> parameter string tuple.
    for i in range(len(columns)):
        treeview.heading(columns[i], text=columns_display[i], anchor="center") # Create new field with a heading
        treeview.column(columns[i], minwidth = 0, width=columns_width, stretch=True, anchor="center") # Settings: data aligned towards center, default width is 100px, and field is stretchable.
        
def search_order(query):
    '''Looks for the employee's query for an order by its ID.'''
    
    # Clear the treeview every time.
    for item in order_search_tree.get_children():
        order_search_tree.delete(item)
    
    # Check if the query is a digit. If it is...
    if query.isdigit():
        # Look for the order by its ID, and return the order.
        order = core.search_order(query) # This can either be a NoneType or an <Order>.
        
        # If the <order> is an instance of <Order>, then insert a row to the treeview that represents the <order>
        # we searched for.
        if isinstance(order, Order):
            order_search_tree.insert('', 'end', values=(order.id, order.customer.name, order.order_items,
                                                        order.invoice_path))
            mb.showinfo('Search successful',
                        f"Your query has been successful! An order has been returned.") # Success message
        # Otherwise, it is probably because the chosen number was too high,
        # compared to the order ID with the biggest value.
        else:
            # Aptly, show a warning message.
            mb.showwarning('Query too high!', f"Your query for an order ID ({query}) equals or exceeds the number of orders ({len(core.orders)}) recorded in our system.")
    # If the query is a blank string, treat this as an action from the user to end the search.
    elif query == "":
        populate_order_search_tree() # Re-populates the treeview with all saved orders.
    # If the query is a non-numeric, and non-blank string, show the user an error message then clear the search.
    else:
        mb.showerror('Incorrect value format',
                f"You have entered a query with an unexpected format ({type(query)}), 0 orders have been found.")
        clear_entries(order_search_entry) # Treat this case as a mistake, and clear the query entry.
        populate_order_search_tree()
        pass

def clear_entries(*args: ttk.Entry):
    for entry in args:
        entry.delete(0, 'end')

def add_book(book_stock, book_price, book_isbn, book_year, book_title, book_author, book_pages, book_genre):
    '''Adds book for tree display and order placing.'''
    # !!! This procedure assumes that there will be no errors throughout its run. !!!
    # The user can run this code by pressing the 'Add' button in the 'Add Book' page.
    
    # 1. Clear all entries.
    clear_entries(title_entry, author_entry, genre_entry, year_entry,
                  pages_entry, stock_entry, price_entry, isbn_entry)
    
    # 2. Always toggle the availability to True,
    # for the book is in stock.
    book_availability = True
    
    # 3. Create a <book_to_add> variable for the system, via core function.
    book_to_add = core.add_book(book_stock, book_availability, book_price, book_isbn, book_year, 
                                book_title, book_author, book_pages, book_genre)
    
    ## Maintenance ##
    # 4. Clear all books from the view tree.
    for tree_book in book_view_tree.get_children():
        book_view_tree.delete(tree_book)
    # 5. Re-insert existing books to the view tree.
    populate_book_view_tree()
    
    mb.showinfo('Add Book', f'Your book "{book_to_add.name}" {ADDED_TO_SYS_MSG}') # Success message

def add_customer(customer_email, customer_phone, customer_name):
    '''Adds customer for tree display and order placing.'''
    # !!! This procedure assumes that there will be no errors throughout its run. !!!
    # The user can run this code by pressing the 'Add' button in the 'Add Customer' page.
    
    # 1. Clear all entries.
    clear_entries(email_entry, phone_entry, name_entry)
    
    # 2. Check if the email entered by the user is in a valid format. If so...
    if core.validate_as_email(customer_email):
        # 3. Create a <customer_to_add> variable for the system, via core function.
        customer_to_add = core.add_customer(customer_email, customer_phone, customer_name)
        
        ############################################### Maintenance ###############################################
        # 4. Clear all customers from the view tree and the order listbox.
        for tree_customer in customer_view_tree.get_children():
            customer_view_tree.delete(tree_customer)        
        order_customer_listbox.delete(0, tk.END)
        
        # 5. Re-insert saved customers to the view tree and listbox.
        populate_customer_view_tree()
        populate_customer_listbox()
        
        mb.showinfo('Add Customer', f'Your customer, {customer_to_add.name}, {ADDED_TO_SYS_MSG}') # Success message
        
    # Otherwise, if the email entered by the user is in an invalid format,
    # then show a warning message to tell them. We do not want to scare the user
    # by giving them error messages for minor mistakes.
    else:
        mb.showwarning("Invalid email address",
                'The email address you\'ve tried to enter is not in the correct format ("jane_doe@example.com").')

def populate_book_view_tree():
    """Populates book_view_tree with rows of books
    (i.e. items in the books list from the core module)."""
    # For every book in the books list,
    for core_book in core.books:
        # If the book stock is more than zero,
        if core_book.stock > 0:
            # insert row into tree, with 'In stock' as the availability field value.
            book_view_tree.insert('', 'end',
                                    values=(core_book.id, core_book.stock, "In stock", core_book.unit_price,
                                            core_book.isbn, core_book.year, core_book.name, core_book.author,
                                            core_book.pages, core_book.genre))
        # Otherwise, if the book stock is zero,
        elif core_book.stock == 0:
            core_book.in_stock = False # The book is out of stock and is unavailable to place orders to.
            # either way, insert row into tree, with 'Out of stock' as the availability field value.
            book_view_tree.insert('', 'end',
                                    values=(core_book.id, core_book.stock, "Out of stock", core_book.unit_price,
                                            core_book.isbn, core_book.year, core_book.name, core_book.author,
                                            core_book.pages, core_book.genre))
        
        # If the book stock is a negative value,
        # which is impossible, do not even consider
        # inserting anything to the tree.
        else:
            pass

def populate_customer_view_tree():
    """Populates customer_view_tree with rows of customers
    (i.e. items in the customers list from the core module)."""
    # For every customer in the customers list,
    for core_customer in core.customers:
        # insert a row of that customer into the tree.
        customer_view_tree.insert('', 'end', values=(core_customer.id, core_customer.email,
                                                       core_customer.phone, core_customer.name))

def populate_order_search_tree():
    """Populates order_search_tree with rows of orders
    (i.e. items in the orders list from the core module)."""
    # For every customer in the customers list,
    for core_order in core.orders:
        # insert a row of that customer into the tree.
        order_search_tree.insert('', 'end',
                                 values=(core_order.id, core_order.customer.name,
                                         core_order.order_items, core_order.invoice_path))

def populate_customer_listbox():
    """Populates customer_listbox with rows of customers' names
    and email in this format "Name (Email)"
    (i.e. the special string value for each customer in
    the customers list from the core module)."""
    # For every customer in the customers list,
    for core_customer in core.customers:
        # insert a row of that customer into the listbox.
        order_customer_listbox.insert(tk.END, core_customer)

def update_product_combobox_options():
    """ Updates product combobox options """
    books_in_stock = [book for book in core.books if book.in_stock == True] # Filters out unavailable books
    order_product_combobox['values'] = tuple(books_in_stock) # Stores available books as combobox options
    
    if len(books_in_stock) > 0:
        order_product_combobox.current(0) # Default for this program

def view_invoice():
    if len(order_search_tree.selection()) > 0:
        # Get the values of the order from the selected tree row
        selected_order_id = order_search_tree.selection()[0]
        selected_order = order_search_tree.item(selected_order_id)
        selected_order_values = selected_order.get("values")
        
        # Get the value from the invoice column
        selected_order_invoice = selected_order_values[3]
        
        # Linear search for matching invoice with an
        # existing order's invoice.
        for order in core.orders:
            if selected_order_invoice == order.invoice_path:
                order.view_invoice()
                break # Breaks the loop
            else:
                print("Let's go!")
    else:
        pass

def add_to_cart():
    """Adds an order item to the cart."""
    
    ######################## Variables ########################
    j = 0 # Index value for book in <books> to add to cart
    bois = core.book_order_items # alias for <book_order_items>
    
    # Get string from order_product_combobox_value, assign it to selected_product
    selected_product = order_product_combobox_value.get()
    selected_product_quantity = order_quantity_value.get()
    
    # Extract title and ISBN from split lists
    sp_title, rest = selected_product.split(' (', 1)
    sp_year, rest2 = rest.split(') by ', 1)
    sp_author, sp_isbn = rest2.split(', ISBN: ', 1)
    
    ######################### Program #########################
    # 1. Search if the selected title and ISBN
    #    match any stored book's title and ISBN from <books>.
    for i in range (len(core.books)):
        if (sp_title == core.book_titles[i] and sp_isbn == core.books[i].isbn):
            break
        else:
            j += 1 # Increment j by 1
    
    bta = core.books[j] # book to add
    
    # 2. Because they will, inevitably, check if the
    #    <order_quantity_spinbox_value> is greater than the book's <stock>
    if core.compare_quantity_and_stock(selected_product_quantity, bta.stock):
        sp_amount = bta.unit_price * selected_product_quantity
        book_order_item = BookOrderItem(bta.id, bta.stock, bta.in_stock, bta.unit_price, bta.isbn, bta.year,
                                        bta.name, bta.author, bta.pages, bta.genre, selected_product_quantity,
                                        sp_amount)
        # 3. If it's less than,
        #    append <book_order_item> to <book_order_items>...
        bois.append(book_order_item)
        # 4. ...then minus <stock> from the <order_quantity_spinbox>
        bta_index = core.books.index(bta)
        core.books[bta_index].stock -= selected_product_quantity
        # 5. Dump modified <books> list to books.pkl
        core.save_books()
    
        # 6. Clear <order_items_tree>
        for tree_item in order_items_tree.get_children():
            order_items_tree.delete(tree_item)
        
        # 7. Insert each <book_order_item> in <book_order_items> to <order_items_tree>.
        for i in range(len(bois)):
            order_items_tree.insert('', 'end', values=((i + 1), bois[i].id, bois[i].name, bois[i].quantity,
                                                    bois[i].unit_price, round(bois[i].amount, 2)))
        
        # 8. Update subtotal and total
        update_totals(bois[-1].amount)
        
        ## Maintenance ##
        # 9. Clear all books from <book_view_tree>
        for tree_book in book_view_tree.get_children():
            book_view_tree.delete(tree_book)
        # 10. Re-populate with updated set of books
        populate_book_view_tree()
    # If the quantity is greater than the stock number, then give a warning message.
    else:
        mb.showwarning('Quantity too high!',
            f'The quantity you\'ve selected exceeds the stock available for "{selected_product}" in the system.')

def update_totals(amount_to_add: float):
    '''Updates the subtotal and total of an order.'''
    # 1. Get subtotal and total from their
    #    StringVars and cast into float numbers
    sub_total = float(order_subtotal_value.get())
    total = float(order_total_value.get())
    
    # 2. Sum up the subtotal and total
    sub_total += amount_to_add
    total += amount_to_add
    
    # 3. Update the StringVar values using setters
    order_subtotal_value.set(f"{float(sub_total):.2f}")
    order_total_value.set(f"{float(total):.2f}")

def toggle_shipping():
    """Toggles the urgent shipping cost on/off when the user checks the 'Urgent?' box."""
    
    # 1. Check if the box is checked, if so...
    if is_urgent.get() == 1:
        # 2. Set the order shipping value to the urgent shipping cost.
        order_shipping_value.set(f"{float(URGENT_SHIPPING_COST):.2f}")
        # 3. Calculate the new order total value, and set <order_total_value> to that sum.
        new_order_total_value = float(order_total_value.get()) + float(order_shipping_value.get())
        order_total_value.set(f"{float(new_order_total_value):.2f}")
    
    # 4. Otherwise, if it is unchecked,
    else:
        # 5. Calculate the new order total value.
        new_order_total_value = float(order_total_value.get()) - float(order_shipping_value.get())
        # 6. Set the order shipping value to the free shipping cost.
        order_shipping_value.set(f"{float(FREE_SHIPPING_COST):.2f}")
        # 7. Set <order_total_value> to that difference.
        order_total_value.set(f"{float(new_order_total_value):.2f}")

def enable_place_order_btn(event):
    """Enables the button to place order."""
    if event.widget.curselection() and core.book_order_items:
        place_order_btn.config(state="normal")
    else:
        place_order_btn.config(state="disabled")

def place_order(order_items, order_total, order_shipping, order_customer, order_sub_total):
    """Places the order."""
    # 1. Reset all selections and values.
    order_customer_listbox.selection_clear(0, tk.END)
    order_quantity_value.set(0)
    order_quantity_spinbox.config(textvariable=order_quantity_value)
    order_subtotal_value.set(f"{float(0):.2f}")
    order_shipping_value.set(f"{float(0):.2f}")
    order_total_value.set(f"{float(0):.2f}")
    
    # 2. Cast all costs into float numbers
    order_total = float(order_total)
    order_shipping = float(order_shipping)
    order_sub_total = float(order_sub_total)
    
    # 3. Return the newly added order.
    order_for_invoice = core.add_order(order_items, order_total, order_shipping, order_customer, order_sub_total)
    
    ## Maintenance ##
    # 4. Clear all orders from the cart...
    for tree_items in order_items_tree.get_children():
        order_items_tree.delete(tree_items)
    #    ... AND the search tree.
    for tree_order in order_search_tree.get_children():
        order_search_tree.delete(tree_order)
    # 5. Re-insert all orders back into the search tree.
    populate_order_search_tree()
    
    # 6. Generate the invoice.
    order_for_invoice.generate_invoice()
    # Confirmation message
    mb.showinfo("Successful order",
                "Your customer's order has been placed successfully! An invoice has been generated.")
    
    # 7. Display the invoice to employee on Excel.
    order_for_invoice.view_invoice()
    
    # 8. Clear the list of <book_order_items> to avoid them piling up in another order.
    core.book_order_items.clear()
    pass

def validate_inputs(*args):
    # 1. Get global variables
    global title_var, author_var, genre_var, year_var, pages_var, stock_var, price_var, isbn_var
    global name_var, email_var, phone_var
    global add_books_btn, add_customer_btn
    
    # 2. Get all variables, and strip out all trailing whitespaces
    # 'Add Books' frame entries
    title = title_var.get().strip()
    author = author_var.get().strip()
    genre = genre_var.get().strip()
    year = year_var.get().strip()
    pages = pages_var.get().strip()
    stock = stock_var.get().strip()
    price = price_var.get().strip()
    isbn = isbn_var.get().strip()
    # 'Add Customers' frame entries
    name = name_var.get().strip()
    email = email_var.get().strip()
    phone = phone_var.get().strip()
    
    # 3. Check if all variables each are in the correct data type.
    # 'Add Books' frame
    if (title and author and genre and year.isdigit() and core.validate_as_float(price)
        and pages.isdigit() and stock.isdigit() and int(year) > 0 and float(price) > 0.00
        and int(stock) > 0 and str(isbn)[:3] == "978" and len(str(isbn)) == 13):
        add_books_btn.config(state="normal")
    else:
        add_books_btn.config(state="disabled")
        
    # 'Add Customers' frame
    if name and email and phone:
        add_customer_btn.config(state="normal")
    else:
        add_customer_btn.config(state="disabled")

def trace_add_vars(*args):
    '''Traces all StringVar/IntVar that are linked to entries
    as the user is typing (or 'writing' data) inside them.'''
    for var in args:
        var.trace_add("write", validate_inputs)

def show_frame(frame):
    """Raises a Tkinter frame."""
    frame.tkraise()
# endregion
###################################################################################################################

###################################################################################################################
###################################################################################################################
# region ######################################### INITIALISING GUI ###############################################
###################################################################################################################
###################################################################################################################

# Setting up window #
window = tk.Tk() # Creates a root window
window.iconbitmap('images/favicon.ico') # Favicon for window
window.title("Milkstones Book Ordering System")

# Panes configurations #
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)

LOGO_IMG = tk.PhotoImage(file="images\\logo.png") # Logo of company

###################################################################################################################
# region ################################## Frame 1: Navigation Side Bar ##########################################
###################################################################################################################
nav = tk.Frame(window, bg="#0076ae", padx=10, pady=10) # Initialise navigation bar as a frame
nav.grid(row=0, column=0, sticky='ns') # Place on grid

# Adding Buttons #
tk.Button(nav, text='Book', command=lambda: show_frame(book_frame), bg="white", fg="#0076ae", font=("Segoe UI", 16, "bold")).pack(fill='x')
tk.Button(nav, text='Customer', command=lambda: show_frame(customer_frame), bg="white", fg="#0076ae", font=("Segoe UI", 16, "bold")).pack(fill='x', pady=10)
tk.Button(nav, text='Orders', command=lambda: show_frame(order_frame), bg="white", fg="#0076ae", font=("Segoe UI", 16, "bold")).pack(fill='x')
# endregion
###################################################################################################################

###################################################################################################################
# region ######################################### Frame 2: Main ##################################################
###################################################################################################################

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++ NOTES: +++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# !!!!!!!!!!!!!!!!!!!!! ALL GUI WIDGETS EXCEPT FRAMES AND BUTTON ELEMENTS MUST HAVE A LABEL !!!!!!!!!!!!!!!!!!!!! #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

main = tk.Frame(window, width=1024) # Initialise main frame
main.grid(row=0, column=1, sticky='nsew') # Place on grid

# region ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ StringVars for Validation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
title_var = tk.StringVar()
author_var = tk.StringVar()
genre_var = tk.StringVar()
year_var = tk.StringVar()
pages_var = tk.StringVar()
stock_var = tk.StringVar()
price_var = tk.StringVar()
isbn_var = tk.StringVar()

name_var = tk.StringVar()
email_var = tk.StringVar()
phone_var = tk.StringVar()

trace_add_vars(title_var, author_var, genre_var, year_var, pages_var, stock_var, price_var, isbn_var, name_var,
               email_var, phone_var)
# endregion
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# region #####################################~~ Frame 2.1: Book, ~~###############################################
############################~~ this is the first frame that will be shown by default ~~############################
# region
book_frame = tk.Frame(main) # Initialising frame
book_frame.grid(row=0, column=0, sticky='nsew') # Setting position

# Notebook tabs setup
book_tabs = ttk.Notebook(book_frame) # Notebook
book_add_frame = ttk.Frame(book_tabs)
book_view_frame = ttk.Frame(book_tabs)
book_tabs.pack(fill="both", expand=True)
book_tabs.add(book_add_frame, text='Add Book', sticky="nsew") # Adds tab for book_add_frame
book_tabs.add(book_view_frame, text='View Book', sticky="nsew") # Adds tab for book_view_frame
# endregion

# region ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 2.1.1 Add Book ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#### Title Label ####
book_add_label = tk.Label(book_add_frame, image=LOGO_IMG, text=" Add Book*",
                          compound="left", font=("Segoe UI", 24, "bold"), foreground="#0076ae") # Added styling
book_add_label.grid(row=0, column=0, columnspan=4, sticky='se') # Adds the label onto the master (<book_add_frame>)

#### GUI for 'Title' Attribute ####
title_entry_label = tk.Label(book_add_frame, text="Title:", anchor="w", justify="left")
title_entry_label.grid(row=1, column=0, sticky='nsw', pady=5)
title_entry = ttk.Entry(book_add_frame, textvariable=title_var) # Entry
title_entry.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=20, ipady=5)

#### GUI for 'Author' Attribute ####
author_entry_label = tk.Label(book_add_frame, text="Author:", anchor="w", justify="left")
author_entry_label.grid(row=1, column=2, sticky='nsw', pady=5)
author_entry = ttk.Entry(book_add_frame, textvariable=author_var)
author_entry.grid(row=2, column=2, columnspan=2, sticky='nsew', padx=20, ipady=5)

#### GUI for 'Genre' Attribute ####
genre_entry_label = tk.Label(book_add_frame, text="Genre:", anchor="w", justify="left")
genre_entry_label.grid(row=3, column=0, sticky='nsw', pady=5)
genre_entry = ttk.Entry(book_add_frame, textvariable=genre_var)
genre_entry.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=20, ipady=5)

#### GUI for 'Year' Attribute ####
year_entry_label = tk.Label(book_add_frame, text="Year:", anchor="w", justify="left")
year_entry_label.grid(row=3, column=2, sticky='nsw', pady=5)
year_entry = ttk.Entry(book_add_frame, width=10, textvariable=year_var)
year_entry.grid(row=4, column=2, sticky='nsw', padx=20, ipady=5)

#### GUI for 'Pages' Attribute ####
pages_entry_label = tk.Label(book_add_frame, text="Pages:", anchor="w", justify="left")
pages_entry_label.grid(row=3, column=3, sticky='nsw', pady=5)
pages_entry = ttk.Entry(book_add_frame, width=5, textvariable=pages_var)
pages_entry.grid(row=4, column=3, sticky='nsw', padx=20, ipady=5)

#### GUI for 'Stock' Attribute ####
stock_entry_label = tk.Label(book_add_frame, text="Stock:", anchor="w", justify="left")
stock_entry_label.grid(row=5, column=0, sticky='nsw', pady=5)
stock_entry = ttk.Entry(book_add_frame, width=5, textvariable=stock_var)
stock_entry.grid(row=6, column=0, sticky='nsw', padx=20, ipady=5)

#### GUI for 'Price' Attribute ####
price_entry_label = tk.Label(book_add_frame, text="Price:", anchor="w", justify="left")
price_entry_label.grid(row=5, column=1, sticky='nsw', pady=5)
price_entry = ttk.Entry(book_add_frame, width=10, textvariable=price_var)
price_entry.grid(row=6, column=1, sticky='nsw', padx=20, ipady=5)

#### GUI for 'ISBN' Attribute ####
isbn_entry_label = tk.Label(book_add_frame, text="ISBN:", anchor="w", justify="left")
isbn_entry_label.grid(row=5, column=2, sticky='nsw', pady=5)
isbn_entry = ttk.Entry(book_add_frame, textvariable=isbn_var)
isbn_entry.grid(row=6, column=2, columnspan=2, sticky='nsew', padx=20, ipady=5)

#### Message for required fields ####
required_fields_b_label = tk.Label(book_add_frame, text=f"*{REQUIRED_MSG}", anchor="w", justify="left")
required_fields_b_label.grid(row=7, column=0, columnspan=3, sticky='nsw')

#### Button to add a book ####
add_books_btn = tk.Button(book_add_frame, text="+", foreground="white", disabledforeground="#003e5a",
                          background="#0076ae", command=lambda:add_book((stock_var.get()), price_var.get(),
                          isbn_var.get(), year_var.get(), title_var.get(), author_var.get(), pages_var.get(),
                          genre_var.get()), state="disabled")
add_books_btn.grid(row=7, column=3, sticky='nse', padx=21, pady=20)
# endregion

# region ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 2.1.2 View Book ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#### Label ####
book_view_label = tk.Label(book_view_frame, image=LOGO_IMG, text=" View Book",
                           compound="left", font=("Segoe UI", 24, "bold"), foreground="#0076ae")
book_view_label.grid(row=0, column=0, columnspan=2, sticky='nsew')

#### Treeview and scrollbar ####

book_view_cols = ("BookId", "BookStock", "BookInStock", "BookPrice", "BookIsbn", "BookYear", "BookTitle",
                    "BookAuthor", "BookPages", "BookGenre") # Column identifiers
book_view_cols_text = ("#", "Stock", "Available?", "Price", "ISBN",
                       "Year", "Title", "Author", "Pages", "Genre") # Column text like how it's displayed.
book_view_tree = ttk.Treeview(book_view_frame, columns=book_view_cols, show="headings")
bvt_vscroll = ttk.Scrollbar(book_view_frame, orient="vertical", command=book_view_tree.yview) # Scrollbar
book_view_tree.configure(yscrollcommand=bvt_vscroll.set) # Adds the yscrollcommand to the tree.
book_view_tree.grid(row=1, column=0, sticky="nsew")
bvt_vscroll.grid(row=1, column=1, sticky="nsw")
make_treeview_heading(book_view_tree, book_view_cols, book_view_cols_text, 140) # Creates the headings
                                                                                # for the treeview.

# If there are books that have been previously saved,
if len(core.books) > 0:
    # then populate book_view_tree with those existing books.
    populate_book_view_tree()
# endregion
# endregion
###################################################################################################################

# region ####################################~~ Frame 2.2: Customer ~~#############################################
###################################################################################################################
# region
customer_frame = tk.Frame(main) # Initialising frame
customer_frame.grid(row=0, column=0, sticky='nsew') # Setting position

# Notebook tabs setup
customer_tabs = ttk.Notebook(customer_frame)
customer_add_frame = ttk.Frame(customer_tabs)
customer_view_frame = ttk.Frame(customer_tabs)
customer_tabs.pack(fill="both", expand=True)
customer_tabs.add(customer_add_frame, text='Add Customer', sticky="nsew") # Adds tab for book_add_frame
customer_tabs.add(customer_view_frame, text='View Customer', sticky="nsew") # Adds tab for book_view_frame
# endregion

# region ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 2.2.1 Add Customer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#### Title Label ####
customer_add_label = tk.Label(customer_add_frame, image=LOGO_IMG, text=" Add Customer*",
                              compound="left", font=("Segoe UI", 24, "bold"), foreground="#0076ae")
customer_add_label.grid(row=0, column=0, columnspan=4, sticky='se')

#### GUI for 'Name' Attribute ####
name_entry_label = tk.Label(customer_add_frame, text="Name:", anchor="w", justify="left")
name_entry_label.grid(row=1, column=0, sticky="nsw", pady=5)
name_entry = ttk.Entry(customer_add_frame, textvariable=name_var)
name_entry.grid(row=2, column=0, columnspan=2, sticky="nsw", padx=20, ipady=5)

#### GUI for 'Email' Attribute ####
email_entry_label = tk.Label(customer_add_frame, text="Email:", anchor="w", justify="left")
email_entry_label.grid(row=1, column=2, sticky="nsw", pady=5)
email_entry = ttk.Entry(customer_add_frame, textvariable=email_var)
email_entry.grid(row=2, column=2, columnspan=2, sticky="nsw", padx=20, ipady=5)

#### GUI for 'Phone' Attribute ####
phone_entry_label = tk.Label(customer_add_frame, text="Phone (format as +44):", anchor="w", justify="left")
phone_entry_label.grid(row=3, column=0, sticky="nsw", pady=5)
phone_entry = ttk.Entry(customer_add_frame, textvariable=phone_var)
phone_entry.grid(row=4, column=0, columnspan=2, sticky="nsw", padx=20, ipady=5)

#### Message for required fields ####
required_fields_c_label = tk.Label(customer_add_frame, text=f"*{REQUIRED_MSG}", anchor="w", justify="left")
required_fields_c_label.grid(row=5, column=0, columnspan=3, sticky='nsw')

#### Button for adding a customer ####
add_customer_btn = tk.Button(customer_add_frame, text="+", state="disabled", foreground="white",
                             disabledforeground="#003e5a", background="#0076ae",
                             command=lambda:add_customer(email_entry.get(), phone_entry.get(), name_entry.get()))
add_customer_btn.grid(row=5, column=3, sticky="nsw", padx=21, pady=20)
# endregion

# region ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 2.2.2 View Customer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#### Label ####
customer_view_label = tk.Label(customer_view_frame, image=LOGO_IMG, text=" View Customer",
                               compound="left", font=("Segoe UI", 24, "bold"), foreground="#0076ae")
customer_view_label.grid(row=0, column=0, columnspan=2, sticky='nsew')

#### Treeview and scrollbar ####
customer_view_cols = ("CustomerId", "CustomerEmail", "CustomerPhone", "CustomerName")
customer_view_cols_text = ("#", "Email", "Phone", "Name")
customer_view_tree = ttk.Treeview(customer_view_frame, columns=customer_view_cols, show="headings")
cvt_vscroll = ttk.Scrollbar(customer_view_frame, orient="vertical", command=customer_view_tree.yview)
cvt_vscroll.grid(row=1, column=1, sticky="nsw")
customer_view_tree.configure(yscrollcommand=cvt_vscroll.set)
customer_view_tree.grid(row=1, column=0, sticky="nsew")
make_treeview_heading(customer_view_tree, customer_view_cols, customer_view_cols_text, 200)
customer_view_tree.column("CustomerName", minwidth=0, width=600, stretch=False) # Makes the customer email column
                                                                                 # 200px.
customer_view_tree.column("CustomerEmail", minwidth=0, width=400, stretch=False)

# If there are customers that have been previously saved,
if len(core.customers) > 0:
    # then populate customer_view_tree with those existing customers.
    populate_customer_view_tree()
# endregion

# endregion
###################################################################################################################

# region #####################################~~ Frame 2.3: Order ~~###############################################
###################################################################################################################
# region
order_frame = tk.Frame(main) # Initialising frame
order_frame.grid(row=0, column=0, sticky='nsew') # Setting position

# Notebook tabs setup
order_tabs = ttk.Notebook(order_frame)
order_place_frame = ttk.Frame(order_tabs)
order_search_frame = ttk.Frame(order_tabs)
order_tabs.pack(fill="both", expand=True)
order_tabs.add(order_place_frame, text='Place Order', sticky="nsew") # Adds tab for order_place_frame
order_tabs.add(order_search_frame, text='Search Order', sticky="nsew") # Adds tab for order_search_frame
# endregion

# region ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 2.3.1 Place Order ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#### Label ####
orders_place_label = tk.Label(order_place_frame, image=LOGO_IMG, text=" Place Order*",
                              compound="left", font=("Segoe UI", 24, "bold"), foreground="#0076ae")
orders_place_label.grid(row=0, column=0, columnspan=4, sticky='nsew')

#### Row 1-2 ####
##### Customer listbox [v] #####
order_customer_listbox_label = tk.Label(order_place_frame, text="Customer")
order_customer_listbox_label.grid(row=1, column=0, sticky="sw")
order_customer_listbox = tk.Listbox(order_place_frame) # Listbox
order_customer_listbox.grid(row=2, column=0, sticky="nsw")
# If there are customers that have been previously saved,
if len(core.customers) > 0:
    # then populate order_customer_listbox with those existing customers.
    populate_customer_listbox()
# Check for the selection event to enable the 'Place' button.
order_customer_listbox.bind("<<ListboxSelect>>", enable_place_order_btn)
##### Label for displaying subtotal cost #####
order_subtotal_label = tk.Label(order_place_frame, text="Subtotal:")
order_subtotal_label.grid(row=1, column=3, sticky="sw")
order_subtotal_value = tk.StringVar()
order_subtotal_value.set(f"{float(0):.2f}")
order_subtotal_value_label = tk.Label(order_place_frame, textvariable=order_subtotal_value)
order_subtotal_value_label.grid(row=2, column=3, sticky="nsw")

#### Row 3-4 ####
##### Product combobox [v] #####
order_product_combobox_label = tk.Label(order_place_frame, text="Product")
order_product_combobox_label.grid(row=3, column=0, sticky="sw", pady=5)
order_product_combobox_value = tk.StringVar()
order_product_combobox = ttk.Combobox(order_place_frame, textvariable=order_product_combobox_value,
                                      postcommand=update_product_combobox_options) # Combobox
order_product_combobox['state'] = 'readonly'
order_product_combobox.grid(row=4, column=0, sticky="nsw", padx=20, ipady=5)

##### Quantity spinbox [↕] #####
order_quantity_value = tk.IntVar(value=0)
order_quantity_spinbox_label = tk.Label(order_place_frame, text="Qty.")
order_quantity_spinbox_label.grid(row=3, column=1, sticky="nse", pady=5)
order_quantity_spinbox = ttk.Spinbox(order_place_frame, from_=0, to=10000000, increment=1, width=5,
                                     textvariable=order_quantity_value) # Spinbox
order_quantity_spinbox.grid(row=4, column=1, sticky="nse", ipady=5)
##### Button for adding a product to the order cart #####
add_product_btn = tk.Button(order_place_frame, text="+", command=add_to_cart,
                            foreground="white", disabledforeground="#003e5a", background="#0076ae")
add_product_btn.grid(row=4, column=2, sticky="nsw")
##### Label for displaying shipping cost #####
order_shipping_label = tk.Label(order_place_frame, text="Shipping:")
order_shipping_label.grid(row=3, column=3, sticky="sw")
order_shipping_value = tk.StringVar()
order_shipping_value.set(f"{float(0):.2f}")
order_shipping_value_label = tk.Label(order_place_frame, textvariable=order_shipping_value)
order_shipping_value_label.grid(row=4, column=3, sticky="nsw")

#### Row 5-7 ####
is_urgent = tk.IntVar()
##### Check button for shipping order #####
order_shipping_checkbox = ttk.Checkbutton(order_place_frame, text="Urgent?", variable=is_urgent,
                                          onvalue=1, offvalue=0, command=toggle_shipping)
order_shipping_checkbox.grid(row=6, column=0, sticky="nsw")
##### Label for displaying total cost #####
order_total_label = tk.Label(order_place_frame, text="Total:")
order_total_label.grid(row=5, column=3, sticky="sw")
order_total_value = tk.StringVar()
order_total_value.set(f"{float(0):.2f}")
order_total_value_label = tk.Label(order_place_frame, textvariable=order_total_value)
order_total_value_label.grid(row=6, column=3, sticky="nsw")
##### Treeview and scrollbar #####
order_items_cols = ("OrderItemNo","ProductNo","ProductName","OrderItemQuantity","OrderItemPrice",
                    "OrderItemAmount")
order_items_cols_text = ("#", "Item ID", "Item Name", "Qty.", "Price", "Amount")
order_items_tree = ttk.Treeview(order_place_frame, columns=order_items_cols, show="headings")
make_treeview_heading(order_items_tree, order_items_cols, order_items_cols_text,200)
order_items_tree.column("OrderItemNo", minwidth=25, width=25, stretch=True)
order_items_tree.column("ProductName", minwidth=575, width=575)
oit_vscroll = ttk.Scrollbar(order_place_frame, orient="vertical", command=order_items_tree.yview)
oit_vscroll.grid(row=7, column=4, sticky='nsw')
order_items_tree.configure(yscrollcommand=oit_vscroll.set)
order_items_tree.grid(row=7, column=0, columnspan=4)

#### Row 8 ####
##### Message for required fields #####
required_fields_o_label = tk.Label(order_place_frame, text=f"*{REQUIRED_MSG}", anchor="w", justify="left")
required_fields_o_label.grid(row=8, column=0)
##### Button for placing an order #####
place_order_btn = tk.Button(order_place_frame, text="Place", state="disabled",
                            foreground="white", disabledforeground="#003e5a", background="#0076ae",
                            command=lambda:place_order(core.book_order_items, order_total_value.get(),
                                                order_shipping_value.get(),
                                                core.customers[order_customer_listbox.curselection()[0]], 
                                                # this points to the **customer from the customers list**,
                                                # which is in the same index as the **item that user selected
                                                # in the listbox before placing the order.**
                                                order_subtotal_value.get()))
place_order_btn.grid(row=8, column=3, sticky="nse")

# endregion #######################################################################################################

# region ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Frame 2.3.2 Search Order ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#### Label ####
orders_search_label = tk.Label(order_search_frame, image=LOGO_IMG, text=" Search Order by ID",
                               compound="left", font=("Segoe UI", 24, "bold"), foreground="#0076ae")
orders_search_label.grid(row=0, column=0, columnspan=6, sticky='nsew')

#### Row 1 ####
##### Search entry and instructions #####
order_search_entry = ttk.Entry(order_search_frame)
order_search_entry.grid(row=1, column=0, sticky='nse')
order_search_entry_btn = tk.Button(order_search_frame, text="Search", foreground="white", background="#0076ae",
                                   disabledforeground="#003e5a",
                                   command=lambda:search_order(order_search_entry.get()))
order_search_entry_btn.grid(row=1, column=1, sticky='nsw')
order_search_instr_label = tk.Label(order_search_frame,
                                    text="Select an order, and click on this button to view invoice -->")
order_search_instr_label.grid(row=1, column=4, sticky='nse')
##### View invoice button #####
view_invoice_btn = tk.Button(order_search_frame, text="View Invoice", state="normal",
                             command=lambda:view_invoice(), foreground="white", disabledforeground="#003e5a",
                             background="#0076ae",)
view_invoice_btn.grid(row=1, column=5)

#### Row 2 ####
##### Treeview #####
order_search_cols = ("OrderId","CustomerName","OrderItems","Invoice")
order_search_cols_text = ("#", "Customer Name", "Ordered Items", "Invoice Path")
order_search_tree = ttk.Treeview(order_search_frame, columns=order_search_cols, show="headings")
ost_vscroll = ttk.Scrollbar(order_search_frame, orient="vertical", command=order_search_tree.yview)
ost_vscroll.grid(row=2, column=6, sticky='nsw')
order_search_tree.configure(yscrollcommand=ost_vscroll.set)
order_search_tree.grid(row=2, column=0, columnspan=6, sticky='nsew')
make_treeview_heading(order_search_tree, order_search_cols, order_search_cols_text,100)
order_search_tree.column("OrderId", minwidth=25, width=50, stretch=False)
# If there are orders that have been previously saved,
if len(core.orders) > 0:
    # then populate order_search_tree with those existing orders.
    populate_order_search_tree()

# endregion #######################################################################################################
# endregion
###################################################################################################################

show_frame(book_frame) # Shows the book frame first.
window.mainloop() # Keeps the window active.

# endregion
###################################################################################################################
# endregion
###################################################################################################################
###################################################################################################################

# region ##########################################################################################################
####### ANNEXED #######
# customer_entry_values = [name_entry.get(), email_entry.get(), phone_entry.get()]
# for entry in customer_entry_values:
#     if entry != "":
#         add_customer_btn.config(state="normal")

#### DEBUG: Example books for place order screen ####
#ex_books = bm.example_order_bois

#### DEBUG: Example book ####
# ex_book = bm.boi_for_order1
# ex_book2 = bm.boi_for_order2
# book_search_tree.insert('', 'end', values=(ex_book.id, ex_book.name, ex_book.author, ex_book.genre, ex_book.year,
#                                            ex_book.unit_price, ex_book.isbn, ex_book.stock, "Available"))
# book_search_tree.insert('', 'end', values=(ex_book2.id, ex_book2.name, ex_book2.author, ex_book2.genre,
#                                            ex_book2.year, ex_book2.unit_price, ex_book2.isbn, ex_book2.stock,
#                                            "Out of stock"))

#### DEBUG: Example customer
# ex_customer = bm.example_order_customer
# customer_view_tree.insert('', 'end', values=
#                           (ex_customer.customer_id, ex_customer.name, ex_customer.email, ex_customer.phone))

#### DEBUG: Example order, this is stage 4, don't do it yet
# we need an approach that will help us with placing invoice buttons
# core.orders = bm.example_orders

# for ex_order in core.orders:
    # order_search_tree.insert('', 'end', values=
    #                          (ex_order.order_id, ex_order.customer.name,
    #                           ex_order.order_items, ex_order.invoice_path))

# def make_notebook(frame):
#     tabs = ttk.Notebook(frame)
#     add_frame = ttk.Frame(tabs)
#     search_frame = ttk.Frame(tabs)
#     return tabs, add_frame, search_frame

# endregion
###################################################################################################################