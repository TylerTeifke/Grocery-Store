#This file will handle viewing the total amount individual customers have spent

#Will determine if an ID exists in the specified table
def validate_id(cursor, id):
    if id == '' or not id.isdecimal():
        print('ID must be a number. Try again')
        print('')
        return False

    query = 'SELECT * FROM Customers WHERE ID = ?'
    value = [id]
    cursor.execute(query, value)

    results = cursor.fetchall()

    if len(results) == 0:
        print('No customer has that ID. Try again')
        print('')
        return False
    
    return True

def main(cursor):
    can_continue = False

    while not can_continue:
        id = input('Enter the ID of the customer: ')
        can_continue = validate_id(cursor, id)

    query = """SELECT SUM(price)
               FROM purchases
	            INNER JOIN products ON purchases.product_ID = products.ID
	            INNER JOIN product_details ON products.details_ID = product_details.ID
	            INNER JOIN customers ON purchases.customer_ID = customers.ID
               WHERE customers.ID = ?;"""
    
    value = [id]
    cursor.execute(query, value)
    result = cursor.fetchone()[0]

    #Will convert a null value into 0
    if result is None:
        result = 0

    print('$' + str(result) + '.00')