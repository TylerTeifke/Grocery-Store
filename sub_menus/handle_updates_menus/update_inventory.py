#This file will handle updating the expiration date of a product in the inventory

#Will determine if an ID exists in the specified table
def validate_id(cursor, id):
    if id == '' or not id.isdecimal():
        print('ID must be a number. Try again')
        print('')
        return False

    query = 'SELECT * FROM Products WHERE ID = ?'
    value = [id]
    cursor.execute(query, value)

    results = cursor.fetchall()

    if len(results) == 0:
        print('Invalid ID. Try again')
        print('')
        return False
    
    return True

#Will make sure the day does not exceed the number of days in the month
def validate_day(day, month):
    days_in_each_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if day > days_in_each_month[month - 1]:
        return False
    return True

#Will be used to validate data involving numbers
def validate_number(number, upper_limit, lower_limit):
    if number == '' or not number.isdecimal():
        return False
    if int(number) > upper_limit or int(number) < lower_limit:
        return False
    return True

#Will be used to validate a date entered
def validate_date(date, cursor, id):
    #Will see if the product is perishable or not
    query = """SELECT product_types.ID
                FROM product_types
                JOIN product_details ON product_types.ID = product_details.type_ID
                JOIN products ON product_details.ID = products.details_ID
                WHERE products.ID = ?"""
    value = [id]
    cursor.execute(query, value)
    result = cursor.fetchone()[0]

    if result == 3:
        print('Non-perishable Items cannot have an expiration date. Try again')
        print('')
        return False

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

def update_expiration_date(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter the ID of the item whose expiration date you want to change: ')
        date = input('Enter new expiration date: ')
        can_continue = validate_id(cursor, id) and validate_date(date, cursor, id)

    query = 'UPDATE Products SET expiration_date = ? WHERE ID = ?'
    values = (date, id)
    cursor.execute(query, values)

    connection.commit()

def main(connection, cursor):
    while True:
        print('Type a number corresponding to the data')
        print('Type [1] to update the expiration date')
        print('Type [2] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 2:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            update_expiration_date(connection, cursor)
        else:
            break