# Customer
class Customer:
  """A class for representing a customer."""
  def __init__(self, id, email, phone, name):
    self.__id = id
    self._email = email
    self._phone = phone
    self._name = name
    
    # Sets the customer's phone number
    # to an appropriate UK format.
    # self.phone = self.__format_phone()
      
  @property
  def id(self):
    return self.__id
  
  @id.setter
  def id(self, new_id):
    self.__id = new_id
      
  @property
  def email(self):
    return self._email
  
  @email.setter
  def email(self, new_email):
    self._email = new_email
      
  @property
  def phone(self):
    return self._phone
  
  @phone.setter
  def phone(self, new_phone):
    self._phone = new_phone
      
  @property
  def name(self):
    return self._name
  
  @name.setter
  def name(self, new_name):
    self._name = new_name
  
  def __str__(self):
    return f"{self._name} ({self._email})"
  
  def __format_phone(self):
    # You need to download <phonenumbers> module using pip or the PyPI like this:
    # py -m pip install phonenumbers
    import phonenumbers
    
    try:
      my_phone = phonenumbers.parse(self._phone)
      national_phone = phonenumbers.format_number(my_phone, phonenumbers.PhoneNumberFormat.NATIONAL)
      return national_phone
    except:
      return ""
    
  def format_phone(self):
    formatted_phone = self.__format_phone()
    
    if formatted_phone != "":
      return formatted_phone
    else:
      return "Unrecognisable number"