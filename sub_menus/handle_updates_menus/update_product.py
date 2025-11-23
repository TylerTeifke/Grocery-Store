#This file will handle updates made to the details of a product, like the price and name

def validate_name(name):
    if name == '':
        print('Invalid name. Try again')
        print('')
        return False
    
    return True

#Will determine if an ID exists in the specified table
def validate_id(cursor, id):
    if id == '' or not id.isdecimal():
        print('ID must be a number. Try again')
        print('')
        return False

    query = 'SELECT * FROM Product_details WHERE ID = ?'
    value = [id]
    cursor.execute(query, value)

    results = cursor.fetchall()

    if len(results) == 0:
        print('Invalid ID. Try again')
        print('')
        return False
    
    return True

#Will update the product's name
def update_name(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter the ID of the product whose name you want to change: ')
        name = input('Enter new name: ')
        can_continue = validate_id(cursor, id) and validate_name(name)

    query = 'UPDATE Product_details SET name = ? WHERE ID = ?'
    values = (name, id)
    cursor.execute(query, values)

    connection.commit()

#Will be used to validate the price of a product
def validate_price(number, upper_limit, lower_limit):
    if number == '' or not number.isdecimal():
        print('Price must be a number. Try again')
        print('')
        return False
    if int(number) > upper_limit or int(number) < lower_limit:
        print('That price is either too high or too low. Try again')
        print('')
        return False
    return True

#Will handle updates to the price
def update_price(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter the ID of the product whose price you want to change: ')
        price = input('Enter new price: ')
        can_continue = validate_id(cursor, id) and validate_price(price, 1000, 1)

    query = 'UPDATE Product_details SET price = ? WHERE ID = ?'
    values = (price, id)
    cursor.execute(query, values)

    connection.commit()

def main(connection, cursor):
    while True:
        print('Type a number corresponding to the data')
        print('Type [1] to update the name')
        print('Type [2] to update the price')
        print('Type [3] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 3:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            update_name(connection, cursor)
        elif int(code) == 2:
            update_price(connection, cursor)
        else:
            break