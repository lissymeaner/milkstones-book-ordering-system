# Modules
import bookstore_core as core
from bookstore__customer import Customer
import xlsxwriter as xlw
import datetime

# Order details
class OrderDetails:
  """Details of an order."""
  def __init__(self, order_items, total, shipping, customer, sub_total):
    self.__order_items = order_items # List of order items
    self._total = total # Overall total of the order
    self._shipping = shipping # Shipping cost for the order
    self.__customer = customer # Customer making the order
    self._sub_total = sub_total # Subtotal of the order
  
  @property
  def order_items(self): return self.__order_items
  
  @order_items.setter
  def order_items(self, new_order_items): self.__order_items = new_order_items
      
  @property
  def total(self): return self._total
  
  @total.setter
  def total(self, new_total): self._total = new_total
  
  @property
  def shipping(self): return self._shipping
  
  @shipping.setter
  def shipping(self, new_shipping): self._shipping = new_shipping
  
  @property
  def customer(self): return self.__customer
  
  @customer.setter
  def customer(self, new_customer): self.__customer = new_customer
  
  @property
  def sub_total(self): return self._sub_total
  
  @sub_total.setter
  def sub_total(self, new_sub_total): self._sub_total = new_sub_total
  
  def _generate_invoice_path(self):
    """Generates an invoice path based on the order of orders that are coming through."""
    # Invoice number
    invoice_no = len(core.orders) + 1
    
    # Format the invoice number
    f_invoice_no = "%03d" % invoice_no
    invoice_file_name = f"invoice_{f_invoice_no}.xlsx" # DEFINING THE FILE NAME
    return invoice_file_name # return the invoice file
  
  def generate_invoice_path(self):
    """Generates an invoice path for an order."""
    invoice_path = fr"Invoices\{self._generate_invoice_path()}"
    return invoice_path

# Order
class Order(OrderDetails):
  """Represents an order, encases OrderDetails with extra information like the ID and the path of an invoice."""
  def __init__(self, id: int, order_items, total, shipping, invoice_path: str, customer, sub_total):
    super().__init__(order_items, total, shipping, customer, sub_total)
    self.__id = id # Identifier
    # self._status = status ; Current status of an order (e.g. "processing", "processed", "failed")
    self._invoice_path = invoice_path # Path of an invoice.

  @property
  def id(self): return self.__id
  
  @id.setter
  def id(self, new_id: int): self.__id = new_id
  
  # @property
  # def status(self): return self._status
  
  # @status.setter
  # def status(self, new_status): self._status = new_status
  
  @property
  def invoice_path(self): return self._invoice_path
  
  @invoice_path.setter
  def invoice_path(self, new_invoice_path): self._invoice_path = new_invoice_path
  
  def generate_invoice(self):
    """Generates an invoice from what the user has selected for their order."""
    
    # Initialise beforehand
    invoice_item_headers = ["#", "ITEM ID", "ITEM NAME", "QTY.", "UNIT PRICE", "AMOUNT"] # Headers for listing order items in a table
    invoice_item_records = [] # List to store any records in here
    INVOICE_ITEMS_HEADER_ROW = 9 # Number of rows
    
    invoice_wb = xlw.Workbook(self._invoice_path) # Initialise invoice workbook
    
    # Formatting templates
    normal_style = invoice_wb.add_format({'bg_color':'#F7FBFD', 'font_size':11, 'font_color':'#0076AE', 'font_name': 'Arial'})
    logo_row_style = invoice_wb.add_format({'bold': True, 'bg_color': '#F7FBFD', 'top':5, 'top_color':'#0076AE', 'font_size':28, 'font_name': 'Bahnschrift', 'font_color':'#0076AE'})
    company_address_row_style = invoice_wb.add_format({'bg_color':'#F7FBFD', 'font_size':11, 'font_color':'#0076AE','bold': True, 'font_name': 'Arial Black', 'align':'top',
                                                  'text_wrap': True})
    heading_style = invoice_wb.add_format({'bg_color':'#F7FBFD', 'font_size':11, 'font_color':'#0076AE', 'font_name': 'Arial', 'bold': True, 'font_size':14, 'indent':2, 'align':'bottom'})
    invoice_info_style = invoice_wb.add_format({'bg_color':'#F7FBFD', 'font_size':11, 'font_color':'#0076AE', 'font_name': 'Arial', 'indent':2})
    header_style = invoice_wb.add_format({'bold': True, 'font_color': 'white', 'font_size':14, 'font_name': 'Arial',
                                          'bg_color':'#0076AE', 'indent':2})
    cost_type_style = invoice_wb.add_format({'bold':True, 'indent':2, 'align':'right', 'bg_color':'#F7FBFD', 'font_size':11, 'font_color':'#0076AE', 'font_name': 'Arial'})
    cost_style = invoice_wb.add_format({'bold':True, 'indent':2,'num_format': '"GBP " #,##0.00', 'bg_color':'#F7FBFD', 'font_size':11, 'font_color':'#0076AE', 'font_name': 'Arial'})
    shipping_cost_style = invoice_wb.add_format({'indent':2,'num_format': '"GBP " #,##0.00', 'bg_color':'#F7FBFD', 'font_size':11, 'font_color':'#0076AE', 'font_name': 'Arial'})
    total_cost_style = invoice_wb.add_format({'num_format': '"GBP " #,##0.00', 'bold': True, 'font_color': 'white', 'font_size':14,
                                          'font_name': 'Arial', 'bg_color':'#0076AE'})
    message_style = invoice_wb.add_format({'font_size':14, 'indent':2, 'align':'bottom', 'bg_color':'#F7FBFD', 'font_color':'#0076AE', 'font_name': 'Arial'})
    submessage_style = invoice_wb.add_format({'font_color':'black', 'indent':2, 'align':'bottom', 'bg_color':'#F7FBFD', 'font_size':11, 'font_name': 'Arial'})
    thank_you_style = invoice_wb.add_format({'font_name': 'Arial Black', 'indent':2, 'bg_color':'#F7FBFD', 'font_size':11, 'font_color':'#0076AE'})
    footer_style = invoice_wb.add_format({'bottom':5, 'bottom_color':'#0076AE', 'font_color':'#0076AE', 'font_name': 'Arial', 'bg_color':'#F7FBFD'})
    
    # Creating the worksheet
    invoice_ws = invoice_wb.add_worksheet() # initialise
    for row in range(24): # Fill area with background colour
      invoice_ws.write_row((row+1), 1, ['']*6, normal_style) # Writes an entire row
    
    # Resizing rows and columns
    invoice_ws.set_row_pixels(0, 25)
    invoice_ws.set_column_pixels(0, 0, 25)
    invoice_ws.set_column_pixels(1, 2, 150)
    invoice_ws.set_column_pixels(3, 3, 425)
    invoice_ws.set_column_pixels(4, 4, 150)
    invoice_ws.set_column_pixels(5, 5, 200)
    invoice_ws.set_column_pixels(6, 6, 250)
    invoice_ws.merge_range("B2:G2", "Milkstones", logo_row_style)
    invoice_ws.merge_range("B3:G3", f"2 Spring Street, London, WE2 8BU\n0844 5577 494", company_address_row_style)
    invoice_ws.write('B4', f"INVOICE # {self.id}", heading_style)
    invoice_ws.write('B5', f"Date: {datetime.date.today().strftime("%d/%m/%Y")}", invoice_info_style) # https://www.geeksforgeeks.org/python/formatting-dates-in-python/
    invoice_ws.write('B6', "BILL TO", heading_style)
    invoice_ws.write('G6', "FOR", heading_style)
    invoice_ws.write('B7', self.customer.name, invoice_info_style)
    invoice_ws.write('G7', "Book stock", invoice_info_style)
    invoice_ws.merge_range('B8:G8', self.customer.email, invoice_info_style)
    invoice_ws.merge_range('B9:G9', self.customer.phone, invoice_info_style)
    
    invoice_ws.set_row_pixels(1, 87)
    invoice_ws.set_row_pixels(2, 80)
    invoice_ws.set_row_pixels(3, 50)
    invoice_ws.set_row_pixels(4, 20)
    invoice_ws.set_row_pixels(5, 80)
    invoice_ws.set_row_pixels(6, 20)
    invoice_ws.set_row_pixels(7, 20)
    invoice_ws.set_row_pixels(8, 67)
    
    for order_item in self.order_items:
      invoice_item_records.append(order_item)
    
    # Calculating row number of total row in the invoice worksheet
    INVOICE_ITEMS_TOTAL_ROW = INVOICE_ITEMS_HEADER_ROW + len(invoice_item_records) + 3
    
    # Create header  
    invoice_ws.write_row(INVOICE_ITEMS_HEADER_ROW, 1, invoice_item_headers, header_style)
    # Resizing rows and columns
    invoice_ws.set_row_pixels(INVOICE_ITEMS_HEADER_ROW, 37)
    invoice_ws.set_row_pixels((INVOICE_ITEMS_TOTAL_ROW - 2), 37)
    invoice_ws.set_row_pixels((INVOICE_ITEMS_TOTAL_ROW - 1), 37)
    invoice_ws.set_row_pixels(INVOICE_ITEMS_TOTAL_ROW, 37)
    invoice_ws.set_row_pixels((INVOICE_ITEMS_TOTAL_ROW + 1), 56)
    invoice_ws.set_row_pixels((INVOICE_ITEMS_TOTAL_ROW + 2), 34)
    invoice_ws.set_row_pixels((INVOICE_ITEMS_TOTAL_ROW + 3), 20)
    invoice_ws.set_row_pixels((INVOICE_ITEMS_TOTAL_ROW + 4), 20)
    invoice_ws.set_row_pixels((INVOICE_ITEMS_TOTAL_ROW + 5), 30)
    invoice_ws.set_row_pixels((INVOICE_ITEMS_TOTAL_ROW + 6), 26)
    invoice_ws.set_row_pixels((INVOICE_ITEMS_TOTAL_ROW + 7), 20)
    
    # Create rows for book items
    for row, item in enumerate(invoice_item_records):
      invoice_ws.set_row_pixels((INVOICE_ITEMS_HEADER_ROW+row+1), 37)
      invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 1, row+1, normal_style)
      invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 2, item.id, normal_style)
      invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 3, item.name, normal_style)
      invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 4, item.quantity, normal_style)
      invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 5, item.unit_price, normal_style)
      invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 6, item.amount, invoice_info_style)
      if row + 1 == len(invoice_item_records):
        invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 1, row+1, normal_style)
        invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 2, item.id, normal_style)
        invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 3, item.name, normal_style)
        invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 4, item.quantity, normal_style)
        invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 5, item.unit_price, normal_style)
        invoice_ws.write((INVOICE_ITEMS_HEADER_ROW+row+1), 6, item.amount, invoice_info_style)
    
    for i in range(0, 4):
      invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW - 2), i+1, '', normal_style)
      invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW - 1), i+1, '', normal_style)
    
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW - 2), 5, 'Subtotal', cost_type_style)
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW - 2), 6, self.sub_total, cost_style)
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW - 1), 5, 'Urgent shipping', cost_type_style)
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW - 1), 6, self.shipping, shipping_cost_style)
    
    # Creating the total row
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW), 1, 'TOTAL COST', header_style)
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW), 2, '', header_style)
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW), 3, '', header_style)
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW), 4, '', header_style)
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW), 5, '', header_style)
    invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW), 6, self.total, total_cost_style)
    
    invoice_ws.merge_range((INVOICE_ITEMS_TOTAL_ROW+1), 1, (INVOICE_ITEMS_TOTAL_ROW+1), 6, 'Make all checks payable to Milkstones', message_style)
    invoice_ws.merge_range((INVOICE_ITEMS_TOTAL_ROW+2), 1, (INVOICE_ITEMS_TOTAL_ROW+2), 6, 'If you have any questions concerning this invoice, use the following contact information:', submessage_style)
    invoice_ws.merge_range((INVOICE_ITEMS_TOTAL_ROW+3), 1, (INVOICE_ITEMS_TOTAL_ROW+3), 6, 'Milkstones Customer Support, 0844 5577 494, support@milkstones.com', submessage_style)
    
    for i in range(0, 6):
      invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW+4), i+1, '', normal_style)
      invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW+6), i+1, '', normal_style)
      invoice_ws.write((INVOICE_ITEMS_TOTAL_ROW+7), i+1, '', footer_style)
      
    invoice_ws.merge_range((INVOICE_ITEMS_TOTAL_ROW+5), 1, (INVOICE_ITEMS_TOTAL_ROW+5), 6, 'THANK YOU FOR YOUR ORDER!', thank_you_style)
    
    invoice_wb.close()
  
  def __open_invoice_path(self):
      import os
      invoice_path = self._invoice_path
      os.startfile(invoice_path)
      
  def view_invoice(self):
      self.__open_invoice_path()

# Order item
class OrderItem:
  """Store items for ordering with this class."""
  def __init__(self, quantity: int, amount):
    self._quantity = quantity # Quantity of an item for ordering
    self._amount = amount # Overall amount to pay a stock of the product, amount = unit_price * quantity
  
  @property
  def quantity(self): return self._quantity
  
  @quantity.setter
  def quantity(self, new_quantity): self._quantity = new_quantity
  
  @property
  def amount(self): return self._amount
  
  @amount.setter
  def amount(self, new_amount): self._amount = new_amount
  
  def __add__(self, other): # Unused, adds together a cost of two distinct order items
    return self._amount + other._amount