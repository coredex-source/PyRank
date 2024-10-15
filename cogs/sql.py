import mysql.connector
import random

def get_mysql_data(host,user,password,database,table):
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
        question = [random_data[1]]
        hints = []
        cursor.execute(f'SELECT Hint1, Hint2, Hint3, Hint4 FROM {table} where Question = \"{question[0]}\"')
        data = cursor.fetchall()
        for i in data[0]:
            if i!= None:
                hints.append(i)
        cursor.execute(f'SELECT Answer FROM {table} where Question = \"{question[0]}\"')
        data = cursor.fetchall()
        expectedOutput = data[0][0]
        conn.close()
        return question, hints, expectedOutput
    except mysql.connector.Error as err:
        return f"Error: {err}"