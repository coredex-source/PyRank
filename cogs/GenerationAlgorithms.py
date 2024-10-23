import random
import subprocess

def generate_testcases(testcase1, testcase2, output_cases=5):
    """
    Parameters:
    - testcase1: First test case.
    - testcase2: Second test case.
    - output_cases: Number of test cases to generate.
    Returns:
    - A list of generated test cases.
    """
    if testcase1 or testcase2 is int:
        output_cases += 30
    else:
        output_cases += 10
    print(output_cases)
    test_cases = []
    if type(testcase1) != type(testcase2):
        raise ValueError("Both test cases must be of the same type.")
    def generate_similar_structure(testcase):
        if isinstance(testcase, list):
            new_list = []
            for element in testcase:
                new_list.append(generate_similar_structure(element))
            return new_list
        elif isinstance(testcase, tuple):
            return tuple(generate_similar_structure(element) for element in testcase)
        elif isinstance(testcase, (int, float)):
            if testcase < 10:
                return random.randint(0, 10) if isinstance(testcase, int) else random.uniform(0, 10)
            else:
                return random.randint(0, 100) if isinstance(testcase, int) else random.uniform(0, 100)
        elif isinstance(testcase, str):
            length = len(testcase)
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
        else:
            return random.choice([testcase1, testcase2])
    
    for _ in range(output_cases):
        chosen_structure = random.choice([testcase1, testcase2])
        test_cases.append(generate_similar_structure(chosen_structure))

    return test_cases

def generate_expectedOutputs(array_tc,data,return_data):
    result_data = []
    for testcase in array_tc:
        data_dict = {}
        for i in range(len(return_data)):
            data_dict[return_data[i]] = testcase[i]

        exec_stat = ["python", "-c", data]
        for i in data_dict:
            exec_stat.append(str(data_dict[i]))
            
        # Running the Python code using subprocess and passing arguments
        result = subprocess.run(
            exec_stat,
            text=True,
            capture_output=True
        )

        output = result.stdout or result.stderr

        result_data.append(output)
    return result_data

def generate_tc_a_pairs(testcase1, testcase2, output_cases=5):
    base_array_tc = generate_testcases(testcase1,testcase2, output_cases)
    array_tc = sort_array(base_array_tc)
    return array_tc

def sort_array(array_tc):
    sorted_array_tc = []
    for i in array_tc:
        if i not in sorted_array_tc:
            sorted_array_tc.append(i)

    return sorted_array_tc
