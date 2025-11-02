import sqlite3

try:
    #Gets user input for new employee
    first_name = input('Enter First Name: ')
    last_name = input('Enter Last Name: ')
    print('Pick a number representing a Position:')
    print('[1] for Cashier')
    print('[2] for Manager')
    print('[3] for Clerk')
    position = input('Enter Position Number: ')
    register = input('Enter Register: ')
    salary = input('Enter Salary: ')
    
    connection = sqlite3.connect('grocery_store.db')
    print('connection opened')

    cursor = connection.cursor()

	# Will get the new employees ID by counting how many employees there are currently, and then incrementing by 1
    cursor.execute("SELECT COUNT(*) FROM employees;")
    id = cursor.fetchone()[0] + 1
    
	#Will insert the new values into the database
    query = "INSERT INTO employees(ID, first_name, last_name, register, position_ID, salary) VALUES(?, ?, ?, ?, ?, ?)"
    values = (id, first_name, last_name, register, position, salary)
    cursor.execute(query, values)
    
    connection.commit()
    cursor.close()

except sqlite3.Error as error:
    print('Error occurred - ', error)

finally:
    if connection:
        connection.close()
        print('connection closed')