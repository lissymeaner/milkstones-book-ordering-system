# Modules
from bookstore__order import OrderItem

# Product
class Product:
  """A class representing a generic product."""
  def __init__(self, id, stock, in_stock, unit_price, name):
    self.__id = id # Identifier
    self.__stock = stock # Number of items in stock.
    self.__in_stock = in_stock # Determines whether the product is in stock or not.
    self._unit_price = unit_price # Price of one product.
    self._name = name # Name of the product. (e.g. title of a book)
    
  @property
  def id(self):
    return self.__id
  
  @id.setter
  def id(self, new_id):
    self.__id = new_id
    
  @property
  def stock(self):
    return self.__stock
  
  @stock.setter
  def stock(self, new_stock):
    self.__stock = new_stock
    
  @property
  def in_stock(self):
    return self.__in_stock
  
  @in_stock.setter
  def in_stock(self, new_in_stock):
    self.__in_stock = new_in_stock  
  
  @property
  def unit_price(self):
    return self._unit_price
  
  @unit_price.setter
  def unit_price(self, new_unit_price):
    self._unit_price = new_unit_price
    
  @property
  def name(self):
    return self._name
  
  @name.setter
  def name(self, new_name):
    self._name = new_name

# Book
class Book(Product):
  """A class representing a generic book. Inherits from Product superclass."""
  def __init__(self, id, stock, in_stock, unit_price, isbn, year, name, author, pages, genre):
    super().__init__(id, stock, in_stock, unit_price, name)
    self._isbn = isbn # International Standard Book Number (ISBN)
    self._year = year # Year of publication
    self._author = author # Author of the book
    self._pages = pages # Number of pages
    self._genre = genre # Genre of the book
          
  @property
  def isbn(self):
    return self._isbn
  
  @isbn.setter
  def isbn(self, new_isbn):
    self._isbn = new_isbn
        
  @property
  def year(self):
    return self._year
  
  @year.setter
  def year(self, new_year):
    self._year = new_year
  
  @property
  def author(self):
    return self._author
  
  @author.setter
  def author(self, new_author):
    self._author = new_author
        
  @property
  def pages(self):
    return self._pages
  
  @pages.setter
  def pages(self, new_pages):
    self._pages = new_pages
        
  @property
  def genre(self):
    return self._genre
  
  @genre.setter
  def genre(self, new_genre):
    self._genre = new_genre
  
  def __str__(self):
    return f'{self._name} ({self._year}) by {self._author}, ISBN: {self._isbn}' # The string value an object will display upon calling __str__

# Book order item  
class BookOrderItem(Book, OrderItem):
  """A class for books as an order item. Inherits from the Book and OrderItem classes."""
  def __init__(self, id, stock, in_stock, unit_price, isbn, year, name, author, pages, genre, quantity, amount):
    Book.__init__(self, id, stock, in_stock, unit_price, isbn, year, name, author, pages, genre)
    OrderItem.__init__(self, quantity, amount)