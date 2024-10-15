from flask import Flask, request, jsonify, render_template
import subprocess
import mysql.connector
import random
import time
import tracemalloc

app = Flask(__name__)

expectedOutput = ""

# Connect to the MySQL database and fetch data.
def get_mysql_data():
    global expectedOutput
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123@123",
            database="MAIN"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM main")
        data = cursor.fetchall()
        random_data = random.choice(data)
        question = [random_data[1]]
        hints = []
        cursor.execute('SELECT Hint1, Hint2, Hint3, Hint4 FROM main where Question = \"{}\"'.format(question[0]))
        data = cursor.fetchall()
        for i in data[0]:
            if i!= None:
                hints.append(i)
        cursor.execute('SELECT Answer FROM main where Question = \"{}\"'.format(question[0]))
        data = cursor.fetchall()
        expectedOutput = data[0][0]
        conn.close()
        return question, hints
    except mysql.connector.Error as err:
        return f"Error: {err}"

# Serve the homepage at the root URL.
@app.route("/")
def home():
    questions, hints = get_mysql_data()
    return render_template("index.html", questions = questions, hints = hints)

# Route to execute the Python code.
@app.route("/run", methods=["POST"])
def run_code():
    try:
        # Receive the JSON payload from the frontend.
        data = request.get_json()
        code = data['code']
        user_input = data.get('input', '')

        # Use subprocess to run the code in a safe environment and provide input.
        tracemalloc.start()
        begin_time = time.time()
        result = subprocess.run(
            ["python", "-c", code],
            input=user_input,
            text=True,
            capture_output=True,
            timeout=5
        )
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_time = end_time - begin_time
        # Return either the result or any errors.
        output = result.stdout or result.stderr
        if output == expectedOutput or output == (expectedOutput + "\n"):
            printout = "Correct\n"+output
            print(total_time, current/1024)
            return jsonify({
                "output": printout
            })
        else:
            printout = "Expected Output:"+ expectedOutput+ "\nYour Output:"+ output
            print(total_time, current/1024)
            return jsonify({
                "output": printout
            })
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Error: Code execution timed out"})
    except Exception as e:
        return jsonify({"output": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
