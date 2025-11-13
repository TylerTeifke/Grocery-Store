#This file will allow the user to see every entry in each table

#Creates a list of employees at the store
def list_employees(cursor):
    #The SQL statement that will get the relevant information about each employee
    query = """SELECT first_name, last_name, Positions.name, salary
                FROM Employees
                JOIN Positions ON Employees.position_ID = Positions.ID;"""
    
    cursor.execute(query)
    results = cursor.fetchall()

    #Will print out all of the results from the SQL query above
    for result in results:
        print('Name:', result[0], result[1] + ',', 'Position:', result[2] + ',', 'Salary: $' + str(result[3]))

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
        else:
            break