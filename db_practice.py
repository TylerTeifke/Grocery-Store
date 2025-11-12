import sqlite3
from math import isnan

# a list of all the registers in the store
registers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
             , 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def validate_name(first_name, last_name):
    if first_name == '' or last_name == '':
        print('Invalid name. Try again')
        print('')
        return False
    
    return True

def validate_employee(first_name, last_name, position, register, salary):
    if validate_name(first_name, last_name) == False:
        return False
    if int(position) < 1 or int(position) > 3:
        print('Invalid position. Try again')
        print('')
        return False
    if position == '1' and register == '':
        print('Cashier must have a register. Try again')
        print('')
        return False
    if position != '1' and register != '':
        print('Managers and Clerks do not have registers. Try again')
        print('')
        return False
    if position == '1' and register not in registers:
        print('Invalid Register. Try again')
        print('')
        return False
    if salary == '' or int(salary) < 1:
        print('Invalid salary. Try again')
        print('')
        return False

    return True

#Gets user input for new employee
def add_employee(connection, cursor):
    can_continue = False

    while can_continue == False:
        first_name = input('Enter First Name: ')
        last_name = input('Enter Last Name: ')
        print('Pick a number representing a Position:')
        print('[1] for Cashier')
        print('[2] for Manager')
        print('[3] for Clerk')
        position = input('Enter Position Number: ')
        register = input('Enter Register (If not cashier, leave blank): ')
        salary = input('Enter Salary: ')

        can_continue = validate_employee(first_name, last_name, position, register, salary)

    if position != '1':
        register = None

    # Will get the new employees ID by counting how many employees there are currently, and then incrementing by 1
    cursor.execute("SELECT COUNT(*) FROM employees;")
    id = cursor.fetchone()[0] + 1
    
	#Will insert the new values into the database
    query = "INSERT INTO employees(ID, first_name, last_name, register, position_ID, salary) VALUES(?, ?, ?, ?, ?, ?)"
    values = (id, first_name, last_name, register, position, salary)
    cursor.execute(query, values)
    
    connection.commit()

#Will search the database to make sure the cashier ID is valid
def validate_cashier(cashier_ID, cursor):
    if cashier_ID == '':
        print('Invalid cashier ID. Try again')
        print('')
        return False

    #Will search the database for cashiers with the user defined ID
    query = "SELECT * FROM employees WHERE position_ID = 1 AND ID = ?"
    values = [cashier_ID]
    cursor.execute(query, values)

    result = cursor.fetchall()

    #If there are no cashiers with the above ID, then the ID is invalid
    if len(result) < 1:
        print('Invalid cashier ID. Try again')
        print('')
        return False
    
    return True

#Will decide if the user inputted valid data for a new customer
def validate_customer(first_name, last_name, cashier_ID, cursor):
    if validate_name(first_name, last_name) == False:
        return False
    if validate_cashier(cashier_ID, cursor) == False:
        return False
    return True

#Gets user input for a new customer
def add_customer(connection, cursor):
    can_continue = False

    while can_continue == False:
        first_name = input('Enter First Name: ')
        last_name = input('Enter Last Name: ')
        cashier_ID = input('Enter Cashier Number: ')

        can_continue = validate_customer(first_name, last_name, cashier_ID, cursor)

    # Will get the new customer's ID by counting how many customers there are currently, and then incrementing by 1
    cursor.execute("SELECT COUNT(*) FROM customers;")
    id = cursor.fetchone()[0] + 1
    
	#Will insert the new values into the database
    query = "INSERT INTO customers(ID, first_name, last_name, employee_ID) VALUES(?, ?, ?, ?)"
    values = (id, first_name, last_name, cashier_ID)
    cursor.execute(query, values)
    
    connection.commit()

#Will make sure the customer ID is valid 
def validate_customer_id(customer_id, cursor):
    #Will make sure the customer ID is an actual number
    if customer_id == '' or not customer_id.isdecimal():
        print('Customer ID must be a number. Try again')
        print('')
        return False
    
    #Will create a list of customers in the database
    query = "SELECT * FROM customers"
    cursor.execute(query)
    result = cursor.fetchall()

    int_id = int(customer_id)

    #There is no valid ID that is less than 1 or greater than the number of customers
    if int_id < 1 or int_id > len(result):
        print('Invalid ID. Try again')
        print('')
        return False

    return True

#Will make sure that an ID is valid
def validate_id(id, table, cursor):
    #Will make sure the ID is an actual number
    if id == '' or not id.isdecimal():
        #Will print out the name of the table without the 's' at the end
        print(table[:len(table) - 1], 'ID must be a number. Try again')
        print('')
        return False
    
    #Will create a list from the database. Since table names cannot be parameterized, I have to
    #make a string with the table name
    query = "SELECT * FROM " + table
    cursor.execute(query)
    result = cursor.fetchall()

    int_id = int(id)

    #There is no valid ID that is less than 1 or greater than the number of entries in a table
    if int_id < 1 or int_id > len(result):
        print('Invalid', table[:len(table) - 1], 'ID. Try again')
        print('')
        return False

    return True

#Will determine if the combination of customer and product IDs is already in the purchases table
def is_duplicate(customer_id, product_id, cursor):
    #Will create a list from the database
    query = "SELECT * FROM Purchases WHERE customer_id = ? AND product_id = ?"
    value = [customer_id, product_id]
    cursor.execute(query, value)
    result = cursor.fetchall()

    #return true if there is already a matching entry in the database
    if len(result) > 0:
        print('This purchase is already in the database, Try again')
        print('')
        return True
    
    return False

#Will validate the purchase information
def validate_purchase(customer_id, product_id, cursor):
    if not validate_id(customer_id, "Customers", cursor) or not validate_id(product_id, "Products", cursor):
        return False
    if is_duplicate(customer_id, product_id, cursor):
        return False
    return True

#Will add a purchase to the database
def add_purchase(connection, cursor):
    can_continue = False

    while not can_continue:
        customer_id = input('Enter customer ID: ')
        product_id = input('Enter product ID: ')

        can_continue = validate_purchase(customer_id, product_id, cursor)
    
	#Will insert the new values into the database
    query = "INSERT INTO purchases(customer_ID, Product_ID) VALUES(?, ?)"
    values = (customer_id, product_id)
    cursor.execute(query, values)

    connection.commit()


# Will be used to make sure the product type ID entered was valid
def validate_product_type(type_ID, cursor):
    if type_ID == '':
        return False
    
    #Will search the database for product types with the user defined ID
    query = "SELECT * FROM product_types WHERE ID = ?"
    values = [type_ID]
    cursor.execute(query, values)

    result = cursor.fetchall()

    #If no product has the matching type, then return false
    if len(result) < 1:
        return False
    
    return True

def validate_product(name, type_ID, price, cursor):
    if name == '':
        print('Invalid name. Try ngain')
        print('')
        return False
    if validate_product_type(type_ID, cursor) == False:
        print('Invalid type ID. Try ngain')
        print('')
        return False
    if price == '' or int(price) < 1:
        print('Invalid price. Try ngain')
        print('')
        return False
    return True

def add_product(connection, cursor):
    can_continue = False

    while can_continue == False:
        name = input('Enter Product Name: ')
        print('Enter a number for a product type')
        print('[1] for dairy')
        print('[2] for meat')
        print('[3] for non-perishables')
        print('[4] for fruit')
        print('[5] for vegetables')
        type_ID = input('Enter Type: ')
        price = input('Enter Price: ')

        can_continue = validate_product(name, type_ID, price, cursor)

    # Will get the new product detail's ID by counting how many product details there are currently, and then incrementing by 1
    cursor.execute("SELECT COUNT(*) FROM product_details;")
    id = cursor.fetchone()[0] + 1
    
	#Will insert the new values into the database
    query = "INSERT INTO product_details(ID, name, type_ID, price) VALUES(?, ?, ?, ?)"
    values = (id, name, type_ID, price)
    cursor.execute(query, values)

    connection.commit()

#Will be used to validate data involving numbers
def validate_number(number, upper_limit, lower_limit):
    if number == '' or not number.isdecimal():
        return False
    if int(number) > upper_limit or int(number) < lower_limit:
        return False
    return True

#Will make sure the day does not exceed the number of days in the month
def validate_day(day, month):
    days_in_each_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if day > days_in_each_month[month - 1]:
        return False
    return True

#Will be used to validate a date entered
def validate_date(date, cursor, details_ID):
    #Will see if a blank date is valid for this specific item
    if date == '':
        query = """SELECT product_types.ID
                    FROM product_types
                    JOIN product_details ON product_types.ID = product_details.type_ID
                    WHERE product_details.ID = ?"""
        value = [details_ID]
        cursor.execute(query, value)
        result = cursor.fetchone()[0]

        if result != 3:
            print('Perishable Items must have an expiration date. Try again')
            print('')
            return False
        else:
            return True
        
        

    if date.count('/') < 2 or date.count('/') > 2:
        print('Invalid date format. Format like mm/dd/yy')
        print('')
        return False
    
    #Will indivdually validate the day, month, and year
    date_details = date.split('/')

    #Will make it so the expiration date is formatted correctley
    if (len(date_details[0]) < 2 or len(date_details[0]) > 2 or 
    len(date_details[1]) < 2 or len(date_details[1]) > 2 or 
    len(date_details[2]) < 2 or len(date_details[2]) > 2):
        print('Invalid date format. Format like mm/dd/yy')
        print('')
        return False
    if validate_number(date_details[0], 12, 1) == False:
        print('Invalid month. Try again')
        print('')
        return False
    if validate_number(date_details[1], 31, 1) == False or validate_day(int(date_details[1]), int(date_details[0])) == False:
        print('Invalid day. Try again')
        print('')
        return False
    if validate_number(date_details[2], 99, 0) == False:
        print('Invalid year. Try again')
        print('')
        return False
    
    return True

def validate_inventory_item(details_ID, date, upper_details_limit, lower_details_limit, cursor):
    if validate_number(details_ID, upper_details_limit, lower_details_limit) == False:
        print('Invalid product ID. Try again')
        print('')
        return False
    if validate_date(date, cursor, details_ID) == False:
        return False
    return True

def add_to_inventory(connection, cursor):
    #Will get the name and ID of all products
    query = "SELECT ID, name FROM product_details"
    cursor.execute(query)
    products = cursor.fetchall()

    if len(products) == 0:
        print('No products to add to the inventory')
        print('')
        return
    
    can_continue = False

    while can_continue == False:
        print('Enter a number for the product you wish to add')
        #Will list all of the products that can be added to the inventory
        for product in products:
            print('Enter [' + str(product[0]) + '] for ' + str(product[1]))
        details_ID = input('Enter Product Number: ')
        date = input('Enter Expiration Date (Leave blank if there is no expiration date): ')

        can_continue = validate_inventory_item(details_ID, date, len(products), 1, cursor)

    #Will enter date as a null value in the database if no number was submitted
    if date == '':
        date = None

    # Will get the new product's ID by counting how many products there are currently, and then incrementing by 1
    cursor.execute("SELECT COUNT(*) FROM products;")
    id = cursor.fetchone()[0] + 1
    
	#Will insert the new values into the database
    query = "INSERT INTO products(ID, details_ID, expiration_date) VALUES(?, ?, ?)"
    values = (id, details_ID, date)
    cursor.execute(query, values)
    
    connection.commit()

try:
    connection = sqlite3.connect('grocery_store.db')
    print('connection opened')
    cursor = connection.cursor()

    while True:

        print('Welcome to the grocery store database, here you can add, delete, and update all records')
        print('Type [1] to add an employee')
        print('Type [2] to add a customer')
        print('Type [3] to add a purchase')
        print('Type [4] to add a product')
        print('Type [5] to add a copy of a product to the inventory')
        print('Type [6] to quit')
        code = input('--> ')
        int_code = int(code)
        
        if int_code == 1:
            add_employee(connection, cursor)
        elif int_code == 2:
            add_customer(connection, cursor)
        elif int_code == 3:
            add_purchase(connection, cursor)
        elif int_code == 4:
            add_product(connection, cursor)
        elif int_code == 5:
            add_to_inventory(connection, cursor)
        else:
            break

    cursor.close()

except sqlite3.Error as error:
    print('Error occurred - ', error)

finally:
    if connection:
        connection.close()
        print('connection closed')