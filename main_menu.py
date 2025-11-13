import sqlite3
import add_entry_menu
import list_entries_menu

try:
    connection = sqlite3.connect('grocery_store.db')
    print('connection opened')
    cursor = connection.cursor()

    while True:
        print('Welcome to the grocery store database, here you can add, delete, and update all records')
        print('Type [1] to add entries')
        print('Type [2] to see lists of entries')
        print('Type [3] to update entries')
        print('Type [4] to delete entries')
        print('Type [5] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 5:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            add_entry_menu.main(connection, cursor)
        elif int(code) == 2:
            list_entries_menu.main(cursor)
        else:
            break

    cursor.close()

except sqlite3.Error as error:
    print('Error occurred - ', error)

finally:
    if connection:
        connection.close()
        print('connection closed')