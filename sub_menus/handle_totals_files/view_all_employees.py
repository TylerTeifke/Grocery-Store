#This file will handle showing the total amount of money each employee makes per hour

def main(cursor):
    query = """SELECT SUM(salary)
               FROM Employees"""
    
    cursor.execute(query)
    result = cursor.fetchone()[0]

    #Will convert a null value into 0
    if result is None:
        result = 0

    print('$' + str(result) + '.00')