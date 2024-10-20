import mysql.connector
import random

def fetch_question__hints(host,user,password,database,table):
    '''
    Parameters:
    - host: SQL hostname
    - user: SQL username
    - password: SQL password
    - database: SQL database name
    - table: SQL table name
    Returns:
    - Fetched data from SQL [Question, hints and expectedOutputs]
    '''
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        data = cursor.fetchall()
        random_data = random.choice(data)
        serial_number = [random_data[0]]
        question = [random_data[1]]
        hints = []
        cursor.execute(f'SELECT Hint1, Hint2, Hint3, Hint4 FROM {table} where Question = \"{question[0]}\"')
        data = cursor.fetchall()
        for i in data[0]:
            if i!= None:
                hints.append(i)
        conn.close()
        return serial_number, question, hints
    except mysql.connector.Error as err:
        return f"Error: {err}"
    
def fetch_output(host,user,password,database,table,serial_number):
    '''
    Parameters:
    - host: SQL hostname
    - user: SQL username
    - password: SQL password
    - database: SQL database name
    - table: SQL table name
    Returns:
    - Fetched data from SQL [Question, hints and expectedOutputs]
    '''
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute(f'SELECT Answer FROM {table} where SNo = \"{serial_number}\"')
        data = cursor.fetchall()
        expectedOutput = data[0][0]
        conn.close()
        return str(expectedOutput)
    except mysql.connector.Error as err:
        return f"Error: {err}"
