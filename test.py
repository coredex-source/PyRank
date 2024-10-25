from cogs import sql, GenerationAlgorithms, ExtraCogs
import json

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

data, return_data = sql.fetch_code(host,user,password,database,table,2)

print(data)
print("")
print(return_data)

t1 = "[3,2]"
t2 = "[1,3]"
array_tc = GenerationAlgorithms.generate_tc_a_pairs(ExtraCogs.convert_value(t1),ExtraCogs.convert_value(t2),10)

print(array_tc)
print(len(array_tc))
print("")

result_data = GenerationAlgorithms.generate_expectedOutputs(array_tc, data, return_data)

print(result_data)
print("")
print(len(result_data))