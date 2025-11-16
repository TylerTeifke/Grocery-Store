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
    #This query will look to see if there is any entity in a foreign table that is connected to the entity
    #in the current table
    query = "SELECT * FROM " + current_table + " JOIN " + foreign_table + " ON " + current_table + ".id = " + foreign_table + "." + current_table[:len(current_table) - 1] + "_ID WHERE " + current_table[:len(current_table) - 1] + "_ID = ?;"
    value = [id]

    cursor.execute(query, value)
    results = cursor.fetchall()

    if len(results) > 0:
        print('Unable to delete that entry as it is connected to another entry.')
        print('Please delete the other entry and try again.')
        print('')
        return False
    
    return True

#Will handle deleting an entry into any table except the purchases table
def delete_employee(connection, cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter Employee ID: ')
        can_continue = validate_id(id, 'Employees', cursor) and check_relations(id, 'Employees', 'Customers', cursor)

    query = 'DELETE FROM Employees WHERE ID = ?'
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
        print('Type [5] to delete a copy of a product in the inventory')
        print('Type [6] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 6:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            delete_employee(connection, cursor)
        else:
            break