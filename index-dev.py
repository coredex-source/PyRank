from flask import Flask, request, jsonify, render_template
import subprocess
from cogs import sql, GenerationAlgorithms
from cogs.ExtraCogs import convert_value
import json

app = Flask(__name__)

def load_creds():
    with open('creds.json', 'r') as file:
        config = json.load(file)
    return config
serial_number = -1
expectedOutput = ""
config = load_creds()
host = config['DB_HOST']
user = config['DB_USER']
password = config['DB_PASSWORD']
database = config['DB_NAME']
table = config['TB_NAME']

# Connect to the MySQL database and fetch data.


# Serve the homepage at the root URL.
@app.route("/")
def home():
    global serial_number
    serial_number, questions, hints = sql.fetch_question__hints(host,user,password,database,table)
    serial_number = serial_number[0]
    return render_template("index.html", questions = questions, hints = hints)

# Route to execute the Python code.
@app.route("/run", methods=["POST"])
def run_code():
    try:
        # Receive the JSON payload from the frontend.
        data = request.get_json()
        code = "import tracemalloc\nimport time\ntracemalloc.start()\nbegin_time = time.time()\n"+data['code']+"\nend_time = time.time()\ntotal_time = end_time - begin_time\ncurrent, peak = tracemalloc.get_traced_memory()\ntracemalloc.stop()\nprint('')\nprint('Memory Usage:',peak/1024,'KB |','Execution time:',total_time)"
        user_input = data.get('input', '')

        # Use subprocess to run the code in a safe environment and provide input.
        result = subprocess.run(
            ["python", "-c", code],
            input=user_input,
            text=True,
            capture_output=True,
            timeout=5
        )
        # Return either the result or any errors.
        output = result.stdout or result.stderr
        try:
            main_output = output.rsplit("Memory",1)
            main_output = main_output[0]
        except:
            main_output = output
        expectedOutput = sql.fetch_output(host,user,password,database,table,serial_number)
        print(GenerationAlgorithms.generate_testcases(convert_value(expectedOutput), convert_value(expectedOutput)))
        if expectedOutput == main_output or (expectedOutput + "\n\n") == main_output:
            printout = "Correct\n"+output
            return jsonify({
                "output": printout
            })
        else:
            printout = "Expected Output:"+ expectedOutput+ "\nYour Output:"+ output
            return jsonify({
                "output": printout
            })
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Error: Code execution timed out"})
    except Exception as e:
        return jsonify({"output": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
