#This file will allow the user to see every entry in each table

#Creates a list of employees at the store
def list_employees(cursor):
    #The SQL statement that will get the relevant information about each employee
    query = """SELECT first_name, last_name, Positions.name, salary, Employees.ID
                FROM Employees
                JOIN Positions ON Employees.position_ID = Positions.ID;"""
    
    cursor.execute(query)
    results = cursor.fetchall()

    #Will print out all of the results from the SQL query above
    for result in results:
        print('Name:', result[0], result[1] + ', ID:', result[4], 'Position:', result[2] + ',', 'Salary: $' + str(result[3]))

#Will print out the names of every customer
def list_customers(cursor):
    #The SQL statement that will get the relevant information about each customer
    query = """SELECT first_name, last_name, ID
                FROM Customers;"""
    
    cursor.execute(query)
    results = cursor.fetchall()

    #Will print out all of the results from the SQL query above
    for result in results:
        print('Name:', result[0], result[1] + ', ID:', result[2])

#Will print out the names of each customer, as well as what they bought
def list_purchases(cursor):
    #The SQL statement that will get the relevant information about each customer and product
    query = """SELECT customers.first_name, customers.last_name, product_details.name, customers.ID, Products.ID
               FROM Purchases
	                JOIN Customers ON Purchases.customer_id = Customers.id
	                JOIN Products ON Purchases.product_id = Products.id
	                JOIN Product_details ON Products.details_id = Product_details.id;"""
    
    cursor.execute(query)
    results = cursor.fetchall()

    #Will print out all of the results from the SQL query above
    for result in results:
        print('Customer Name:', result[0], result[1] + ', Customer ID:', str(result[3]) + ', Purchase:', result[2] + ', Purchase ID:', result[4])

#Will print out the products that can be sold at the store
def list_products(cursor):
    #The SQL statement that will get the relevant information about each product
    query = """SELECT name, type, price, Product_Details.ID
               FROM Product_Details
	            JOIN Product_Types ON Product_Details.type_ID = Product_Types.id;"""
    
    cursor.execute(query)
    results = cursor.fetchall()

    #Will print out all of the results from the SQL query above
    for result in results:
        print('Name:', result[0] + ',', 'Type:', result[1] + ',', 'Price: $' + str(result[2]) + ', ID:', result[3])

#Will print out the products that are actually available, as well as their expiration date
def list_available_products(cursor):
    #The SQL statement that will get the relevant information about each product
    query = """SELECT name, expiration_date, Products.ID
               FROM Products
	            JOIN Product_Details ON Products.details_ID = Product_Details.ID;"""
    
    cursor.execute(query)
    results = cursor.fetchall()

    #Will print out all of the results from the SQL query above
    for result in results:
        print('Name:', result[0] + ', ID:', str(result[2]) + ', Expiration Date:', result[1])

def main(cursor):
    while True:
        print('Welcome to the list menu. Here you can see lists of the entries in each table of the database')
        print('Type [1] to see employees')
        print('Type [2] to see customers')
        print('Type [3] to see purchases')
        print('Type [4] to see products')
        print('Type [5] to see currently available products')
        print('Type [6] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 6:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            list_employees(cursor)
        elif int(code) == 2:
            list_customers(cursor)
        elif int(code) == 3:
            list_purchases(cursor)
        elif int(code) == 4:
            list_products(cursor)
        elif int(code) == 5:
            list_available_products(cursor)
        else:
            break