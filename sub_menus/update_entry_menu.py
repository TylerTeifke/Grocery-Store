from sub_menus.handle_updates_menus import handle_customer_updates, handle_employee_update

#This file will handle updating the information in an entry
def update_purchase(connection, cursor):
    return True

def update_product(connection, cursor):
    return True

def update_inventory(connection, cursor):
    return True

def main(connection, cursor):
    while True:
        print('Welcome to the update menu. Here you can update existing entries in the database')
        print('Type [1] to update employees')
        print('Type [2] to update customers')
        print('Type [3] to update purchases')
        print('Type [4] to update products')
        print('Type [5] to update currently available products')
        print('Type [6] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 6:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            handle_employee_update.main(connection, cursor)
        elif int(code) == 2:
            handle_customer_updates.main(connection, cursor)
        elif int(code) == 3:
            update_purchase(connection, cursor)
        elif int(code) == 4:
            update_product(connection, cursor)
        elif int(code) == 5:
            update_inventory(connection, cursor)
        else:
            break