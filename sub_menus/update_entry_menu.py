#This file will handle updating the information in an entry
from sub_menus.handle_updates_menus import update_customer, update_employee, update_purchase, update_product, update_inventory

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
            update_employee.main(connection, cursor)
        elif int(code) == 2:
            update_customer.main(connection, cursor)
        elif int(code) == 3:
            update_purchase.main(connection, cursor)
        elif int(code) == 4:
            update_product.main(connection, cursor)
        elif int(code) == 5:
            update_inventory.main(connection, cursor)
        else:
            break