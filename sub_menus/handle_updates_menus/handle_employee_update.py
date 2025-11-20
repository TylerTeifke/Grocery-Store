#This file will handle all aspects of updating an employee's entry in the database

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
        id = input('Enter the ID of the employee whose name you want to change: ')
        name = input('Enter new ' + type + ' name: ')
        can_continue = validate_id(cursor, id, 'Employees') and validate_name(name)

    query = 'UPDATE Employees SET ' + type + '_name = ? WHERE ID = ?'
    values = (name, id)
    cursor.execute(query, values)

    connection.commit()

def validate_register(register):
    # a list of all the registers in the store
    registers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
             , 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    if register not in registers:
        print('Invalid register. Try again')
        print('')
        return False
    
    return True

#Will check to see if the employee is a cashier.
#If not then their register cannot be changed because they do not have one
def validate_position(cursor, id):
    query = 'SELECT * FROM Employees WHERE ID = ? AND Position_ID = 1'
    value = [id]
    cursor.execute(query, value)
    results = cursor.fetchall()

    if len(results) == 0:
        print('That employee is not a cashier. Try again')
        print('')
        return False
    
    return True

#Will handle changing an employees register
def update_register(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter the ID of the employee whose register you want to change: ')
        register = input('Enter new register: ')
        can_continue = validate_id(cursor, id, 'Employees') and validate_position(cursor, id) and validate_register(register)

    query = 'UPDATE Employees SET register = ? WHERE ID = ?'
    values = (register, id)
    cursor.execute(query, values)

    connection.commit()

#Will check to see if an employee is currently helping a customer.
#If so, then their position cannot be changed
def is_connected(cursor, id):
    query = 'SELECT * FROM Customers WHERE employee_ID = ?'
    value = [id]
    cursor.execute(query, value)

    results = cursor.fetchall()

    if len(results) > 0:
        print('This employee is currently helping a customer, their position cannot be changed')
        print('')
        return True
    
    return False

#Will update an employee's position in the company
def update_position(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter the ID of the employee whose position you want to change: ')
        print('Type [1] for Cashier')
        print('Type [2] for Manager')
        print('Type [3] for Clerk')
        position_id = input('Enter new position: ')
        can_continue = validate_id(cursor, id, 'Employees') and validate_id(cursor, position_id, 'Positions') and not is_connected(cursor, id)

    query = 'UPDATE Employees SET position_id = ? WHERE ID = ?'
    values = (position_id, id)
    cursor.execute(query, values)

    #If the employee is no longer a cashier, then they do not need to be assigned 
    #a cash register
    if int(position_id) != 1:
        query = 'UPDATE Employees SET register = NULL WHERE ID = ?'
        values = [id]
        cursor.execute(query, values)

    connection.commit()

#Will make sure the new salary is valid
def validate_salary(salary):
    if salary == '' or not salary.isdecimal():
        print('Salary must be a number. try again')
        print('')
        return False
    
    if int(salary) <= 0:
        print('Salary must greater than 0. try again')
        print('')
        return False
    
    return True

#Will handle updates to an employee's salary
def update_salary(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter the ID of the employee whose salary you want to change: ')
        salary = input('Enter new salary: ')
        can_continue = validate_id(cursor, id, 'Employees') and validate_salary(salary)

    query = 'UPDATE Employees SET salary = ? WHERE ID = ?'
    values = (salary, id)
    cursor.execute(query, values)

    connection.commit()

def main(connection, cursor):
    while True:
        print('Type a number corresponding to the data')
        print('Type [1] to update the first name')
        print('Type [2] to update the last name')
        print('Type [3] to update the register')
        print('Type [4] to update the position')
        print('Type [5] to update the salary')
        print('Type [6] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 6:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            update_name(connection, cursor, 'first')
        elif int(code) == 2:
            update_name(connection, cursor, 'last')
        elif int(code) == 3:
            update_register(connection, cursor)
        elif int(code) == 4:
            update_position(connection, cursor)
        elif int(code) == 5:
            update_salary(connection, cursor)
        else:
            break