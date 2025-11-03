import sqlite3

# a list of all the registers in the store
registers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
             , 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def validate_employee(first_name, last_name, position, register, salary):
    if first_name == '' or last_name == '':
        print('Invalid name. Try again')
        print('')
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
        print('Type [5] to quit')
        code = input('--> ')
        int_code = int(code)
        
        if int_code == 1:
            #print('test')
            add_employee(connection, cursor)
        else:
            break

    cursor.close()

except sqlite3.Error as error:
    print('Error occurred - ', error)

finally:
    if connection:
        connection.close()
        print('connection closed')