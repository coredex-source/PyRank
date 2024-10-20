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
        break

demo_testcase = [3,2]
data_dict = {}
for i in range(len(return_data)):
    data_dict[return_data[i]] = demo_testcase[i]

exec_stat = ["python", "-c", data]
for i in data_dict:
    exec_stat.append(str(data_dict[i]))
    
# Running the Python code using subprocess and passing arguments
result = subprocess.run(
    exec_stat,
    text=True,
    capture_output=True,
    timeout=5
)

output = result.stdout or result.stderr

print(output)