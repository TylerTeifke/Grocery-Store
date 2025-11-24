import sqlite3
from sub_menus import add_entry_menu, list_entries_menu, delete_entry_menu, update_entry_menu, view_totals_menu

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
        print('Type [5] to view totals')
        print('Type [6] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 6:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            add_entry_menu.main(connection, cursor)
        elif int(code) == 2:
            list_entries_menu.main(cursor)
        elif int(code) == 3:
            update_entry_menu.main(connection, cursor)
        elif int(code) == 4:
            delete_entry_menu.main(connection, cursor)
        elif int(code) == 5:
            view_totals_menu.main(cursor)
        else:
            break

    cursor.close()

except sqlite3.Error as error:
    print('Error occurred - ', error)

finally:
    if connection:
        connection.close()
        print('connection closed')