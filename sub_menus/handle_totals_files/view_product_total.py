#This file will handle showing the total amount of money all available products cost

def main(cursor):
    query = """SELECT SUM(price)
               FROM products
	            INNER JOIN product_details ON products.details_ID = product_details.ID"""
    
    cursor.execute(query)
    result = cursor.fetchone()[0]

    #Will convert a null value into 0
    if result is None:
        result = 0

    print('$' + str(result) + '.00')