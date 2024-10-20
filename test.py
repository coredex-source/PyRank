import json
import mysql.connector
import subprocess

def load_creds():
    with open('creds.json', 'r') as file:
        config = json.load(file)
    return config
config = load_creds()
host = config['DB_HOST']
user = config['DB_USER']
password = config['DB_PASSWORD']
database = config['DB_NAME']
table = config['TB_NAME']

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conn.cursor()

cursor.execute("SELECT code from main where SNo = 2")
data = cursor.fetchone()
data = data[0]

n = 3
k = 2
# Running the Python code using subprocess and passing arguments
result = subprocess.run(
    ["python", "-c", data, str(n), str(k)],
    text=True,
    capture_output=True,
    timeout=5
)

output = result.stdout or result.stderr

print(output)
