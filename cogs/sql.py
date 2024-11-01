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
        cursor = conn.cursor(buffered=True)
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
        cursor = conn.cursor(buffered=True)
        cursor.execute(f'SELECT Answer FROM {table} where SNo = {serial_number}')
        data = cursor.fetchall()
        expectedOutput = data[0][0]
        conn.close()
        return str(expectedOutput)
    except mysql.connector.Error as err:
        return f"Error: {err}"

def fetch_code(host,user,password,database,table,serial_number):
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
        cursor = conn.cursor(buffered=True)
        cursor.execute(f'SELECT code from {table} where SNo = {serial_number}')
        data = cursor.fetchone()
        data = data[0]
        new_data = data.split("\n")
        for i in range(len(new_data)):
            if "def main" in new_data[i]:
                new_data = new_data[i]
                new_data = new_data.rsplit("(")
                new_data = new_data[1]
                new_data = new_data.rsplit(")")
                new_data = new_data[0]
                return_data = []
                for i in new_data:
                    if i != "," and i != " ":
                        return_data.append(i)
                return data, return_data
    except mysql.connector.Error as err:
        return f"Error: {err}"
    
def fetch_creds(host,user,password,database,table,entry):
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
        cursor = conn.cursor(buffered=True)
        try:
            cursor.execute(f'SELECT Email,UName,Password FROM {table} where UName = \'{entry}\' or Email = \'{entry}\'')
            data = cursor.fetchall()
            try:
                user_email = data[0][0]
                user_name = data[0][1]
                user_password = data[0][2]
            except:
                user_email = None
                user_name = None
                user_password = None
        except:
            user_email = None
            user_name = None
            user_password = None
        conn.close()
        return user_email, user_name, user_password
    except mysql.connector.Error as err:
        return f"Error: {err}"