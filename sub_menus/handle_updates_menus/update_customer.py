#This file will handle all updates made to customers

def validate_name(name):
    if name == '':
        print('Invalid name. Try again')
        print('')
        return False
    
    return True

#Will determine if an ID exists in the specified table
def validate_id(cursor, id, table):
    if id == '' or not id.isdecimal():
        print(table, 'ID must be a number. Try again')
        print('')
        return False

    query = 'SELECT * FROM ' + table + ' WHERE ID = ?'
    value = [id]
    cursor.execute(query, value)

    results = cursor.fetchall()

    if len(results) == 0:
        print('Invalid ID. Try again')
        print('')
        return False
    
    return True

#This method will handle updating both the first and last names
def update_name(connection, cursor, type):
    can_continue = False

    while not can_continue:
        id = input('Enter the ID of the customer whose name you want to change: ')
        name = input('Enter new ' + type + ' name: ')
        can_continue = validate_id(cursor, id, 'Customers') and validate_name(name)

    query = 'UPDATE Customers SET ' + type + '_name = ? WHERE ID = ?'
    values = (name, id)
    cursor.execute(query, values)

    connection.commit()

#Will make sure the employee ID is both valid and is attached to a cashier
def validate_cashier(cursor, id):
    if not validate_id(cursor, id, 'Employees'):
        return False
    
    query = 'SELECT * FROM Employees WHERE ID = ? AND position_ID = 1'
    value = [id]
    cursor.execute(query, value)

    result = cursor.fetchall()

    if len(result) < 1:
        print('That employee is not a cashier. Try again')
        print('')
        return False
    
    return True

#Will change which cashier a customer is assigned to
def update_cashier(connection, cursor):
    can_continue = False

    while not can_continue:
        customer_id = input('Enter the ID of the customer you wish to update: ')
        cashier_id = input('Enter the ID of the cashier you wish to assign to the customer: ')

        can_continue = validate_id(cursor, customer_id, 'Customers') and validate_cashier(cursor, cashier_id)

    query = 'UPDATE Customers SET Employee_ID = ? WHERE ID = ?'
    values = (cashier_id, customer_id)
    cursor.execute(query, values)

    connection.commit()

def main(connection, cursor):
    while True:
        print('Type a number corresponding to the data')
        print('Type [1] to update the first name')
        print('Type [2] to update the last name')
        print('Type [3] to update the cashier they are assigned')
        print('Type [4] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 4:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            update_name(connection, cursor, 'first')
        elif int(code) == 2:
            update_name(connection, cursor, 'last')
        elif int(code) == 3:
            update_cashier(connection, cursor)
        else:
            break