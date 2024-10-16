import random

def generate_testcases(testcase1, testcase2, output_cases=5):
    """
    Parameters:
    - testcase1: First test case.
    - testcase2: Second test case.
    - output_cases: Number of test cases to generate.
    Returns:
    - A list of generated test cases.
    """

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
