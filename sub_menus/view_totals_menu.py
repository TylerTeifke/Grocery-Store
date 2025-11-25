#This file will allow the user to find all of the totals of various entries.
#Like the total amount of money a customer has spent

from sub_menus.handle_totals_files import view_customer_totals, view_all_customers, view_all_employees, view_product_total

def main(cursor):
    while True:

        print('Welcome to the totals menu.')
        print('Type [1] to view the total amount of money one customer has spent')
        print('Type [2] to view the total amount of money all customers have spent')
        print('Type [3] to view the total amount of money all employees make')
        print('Type [4] to view the total amount cost of all products')
        print('Type [5] to quit')
        code = input('--> ')
        
        if code == '' or not code.isdecimal() or int(code) < 1 or int(code) > 5:
            print('Invalid code. Try again')
            print('')
        elif int(code) == 1:
            view_customer_totals.main(cursor)
        elif int(code) == 2:
            view_all_customers.main(cursor)
        elif int(code) == 3:
            view_all_employees.main(cursor)
        elif int(code) == 4:
            view_product_total.main(cursor)
        else:
            break