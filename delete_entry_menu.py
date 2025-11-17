#This file will handle deleting entries from the database

#Will make sure an id entered by the user is valid
def validate_id(id, table, cursor):
    if id == '' or not id.isdecimal():
        print('ID must be a number. Try again')
        print('')
        return False
    
    #Will create a list from the database. Since table names cannot be parameterized, I have to
    #make a string with the table name
    query = "SELECT * FROM " + table + " WHERE ID = ?"
    value = [id]
    cursor.execute(query, value)
    result = cursor.fetchall()

    #If no entry has the matching ID, then the ID is invalid
    if len(result) < 1:
        print('Invalid', table[:len(table) - 1], 'ID. Try again')
        print('')
        return False

    return True

#Will check to see if the entry ID is a foreign key in any other table
def check_relations(id, current_table, foreign_table, cursor):
    #Will be used to concatenate the name of the current table in the query
    concat_table = ""

    if current_table == 'Product_details':
        concat_table = current_table[8:]
    else:
        concat_table = current_table[:len(current_table) - 1]

    #This query will look to see if there is any entity in a foreign table that is connected to the entity
    #in the current table
    query = "SELECT * FROM " + current_table + " JOIN " + foreign_table + " ON " + current_table + ".id = " + foreign_table + "." + concat_table + "_ID WHERE " + concat_table + "_ID = ?;"
    value = [id]

    cursor.execute(query, value)
    results = cursor.fetchall()

    if len(results) > 0:
        print('Unable to delete that entry as it is connected to another entry in the ' + foreign_table + ' table.')
        print('Please delete the other entry and try again.')
        print('')
        return False
    
    return True

#Will handle deleting an entry from the employee table
def delete_employee(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter Employee ID: ')
        can_continue = validate_id(id, 'Employees', cursor) and check_relations(id, 'Employees', 'Customers', cursor)

    query = 'DELETE FROM Employees WHERE ID = ?'
    value = [id]
    cursor.execute(query, value)

    connection.commit()

#Will handle deleting an entry from the customer table
def delete_customer(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter Customer ID: ')
        can_continue = validate_id(id, 'Customers', cursor) and check_relations(id, 'Customers', 'Purchases', cursor)

    query = 'DELETE FROM Customers WHERE ID = ?'
    value = [id]
    cursor.execute(query, value)

    connection.commit()

#Will check to see if the customer and product ID's entered for deleting
#a purchase are valid and are in the purchases table
def validate_purchase(customer_id, product_id, cursor):
    if customer_id == '' or not customer_id.isdecimal() or product_id == '' or not product_id.isdecimal():
        print("One of the ID's is invalid. Try again")
        print("")
        return False
    
    query = "SELECT * FROM Purchases WHERE customer_ID = ? AND product_ID = ?"
    values = (customer_id, product_id)
    cursor.execute(query, values)
    results = cursor.fetchall()

    if len(results) < 1:
        print("There are no purchases involving that customer and product. Try again.")
        print("")
        return False
    
    return True

#Will handle deleting an entry from the purchase table
def delete_purchase(connection, cursor):
    can_continue = False

    while not can_continue:
        customer_id = input('Enter Customer ID: ')
        product_id = input('Enter Product ID: ')
        can_continue = validate_purchase(customer_id, product_id, cursor)

    query = 'DELETE FROM Purchases WHERE customer_ID = ? AND product_ID = ?'
    value = (customer_id, product_id)
    cursor.execute(query, value)

    connection.commit()

#Will handle deleting an entry from the product_details table
def delete_product(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter Product ID: ')
        can_continue = validate_id(id, 'Product_details', cursor) and check_relations(id, 'Product_details', 'Products', cursor)

    query = 'DELETE FROM Product_details WHERE ID = ?'
    value = [id]
    cursor.execute(query, value)

    connection.commit()

#Will handle deleting an entry from the products table
def delete_from_inventory(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter Inventory ID: ')
        can_continue = validate_id(id, 'Products', cursor) and check_relations(id, 'Products', 'Purchases', cursor)

    query = 'DELETE FROM Products WHERE ID = ?'
    value = [id]
    cursor.execute(query, value)

    connection.commit()

def main(connection, cursor):
    while True:

        print('Welcome to the delete menu. Type the specified number to delete an entry from a table')
        print('Type [1] to delete an employee')
        print('Type [2] to delete a customer')
        print('Type [3] to delete a purchase')
        print('Type [4] to delete a product')
        print('Type [5] to delete a copy of a product from the inventory')
        print('Type [6] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 6:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            delete_employee(connection, cursor)
        elif int(code) == 2:
            delete_customer(connection, cursor)
        elif int(code) == 3:
            delete_purchase(connection, cursor)
        elif int(code) == 4:
            delete_product(connection, cursor)
        elif int(code) == 5:
            delete_from_inventory(connection, cursor)
        else:
            break