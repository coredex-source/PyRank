from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import subprocess
from cogs import sql, GenerationAlgorithms
from cogs.ExtraCogs import convert_value
import json

app = Flask(__name__)
app.secret_key = '4f9f1aed-0324-400a-b204-e03ac8c752b5-56d3d24b-b0b4-4635-8482-ee8da0996763-2420a60a-1b81-45c7-82a1-317c96681a9a'

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

# Login route
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("username")
    password = request.form.get("password")
    
    # Check credentials to be replaced by sql later
    if email == config.get("EMAIL") and password == config.get("PASSWORD"):
        session['user'] = email  # Mark the user as logged in
        return redirect(url_for("home"))
    else:
        return "Invalid credentials, please try again.", 401

@app.route("/")
def home():
    if 'user' not in session:
        return redirect(url_for("show_login"))
    
    global serial_number
    serial_number, questions, hints = sql.fetch_question__hints(host, user, password, database, table)
    serial_number = serial_number[0]
    return render_template("index.html", questions=questions, hints=hints)

# Display login page
@app.route("/show_login")
def show_login():
    return render_template("login.html")

# Display signup page
@app.route("/show_signup")
def show_signup():
    return render_template("signup.html")

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
