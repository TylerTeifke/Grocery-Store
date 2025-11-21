#This file will handle updates made to a purchase

#Will determine if the specified ID exists in the specified table
def validate_id(cursor, id, table):
    if id == '' or not id.isdecimal():
        print(table[:len(table) - 1], 'ID must be a number. Try again')
        print('')
        return False

    #Will make sure that any table has a matching ID to the id parameter
    query = 'SELECT * FROM ' + table +  ' WHERE ID = ?'
    value = [id]
    cursor.execute(query, value)

    results = cursor.fetchall()

    if len(results) == 0:
        print('ID is not in ' + table + '. Try again')
        print('')
        return False
    
    return True

#Will determine if the specified customer and product IDs exist together in the purchases table
def validate_purchase(cursor, customer_id, product_id):
    if customer_id == '' or not customer_id.isdecimal() or product_id == '' or not product_id.isdecimal():
        print('The customer and product IDs must both be numbers. Try again')
        print('')
        return False

    #Will make sure that the Purchases table contains both of the IDs
    query = 'SELECT * FROM Purchases WHERE customer_ID = ? AND product_ID = ?'
    values = (customer_id, product_id)
    cursor.execute(query, values)

    results = cursor.fetchall()

    if len(results) == 0:
        print('Invalid customer or purchase ID. Try again')
        print('')
        return False
    
    return True

#Will determine if the combination of customer and product IDs is already in the purchases table
def is_duplicate(cursor, customer_id, product_id):
    #Will create a list from the database
    query = "SELECT * FROM Purchases WHERE customer_id = ? AND product_id = ?"
    values = [customer_id, product_id]
    cursor.execute(query, values)
    result = cursor.fetchall()

    #return true if there is already a matching entry in the database
    if len(result) > 0:
        print('This purchase is already in the database, Try again')
        print('')
        return True
    
    return False

#Will handle updates made to both the customer and product IDs
def update(connection, cursor, changed_table):
    can_continue = False

    #Will hold the singular form of the table name, so that it can be used in a query
    changed_id = changed_table[:len(changed_table) - 1] + '_ID'

    while not can_continue:
        customer_id = input('Enter the customer ID for the purchase: ')
        product_id = input('Enter the product ID for the purchase: ')
        new_id = input('Now enter the new ID for the ' + changed_table[:len(changed_table) - 1] + ': ')

        #Will check to see if the new customer/product ID creates a duplicate in the purchases table
        duplicate = True
        if(changed_table == 'Customers'):
            duplicate = is_duplicate(cursor, new_id, product_id)
        else:
            duplicate = is_duplicate(cursor, customer_id, new_id)

        can_continue = validate_purchase(cursor, customer_id, product_id) and validate_id(cursor, new_id, changed_table) and not duplicate

    query = 'UPDATE Purchases SET ' + changed_id + ' = ? WHERE customer_ID = ? AND product_ID = ?'
    values = (new_id, customer_id, product_id)
    cursor.execute(query, values)

    connection.commit()

def main(connection, cursor):
    while True:
        print('Type a number corresponding to the data')
        print('Type [1] to update the customer')
        print('Type [2] to update the product')
        print('Type [3] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 3:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            update(connection, cursor, 'Customers')
        elif int(code) == 2:
            update(connection, cursor, 'Products')
        else:
            break