import time
import tracemalloc

# Example function to analyze
def example_function(n):
    # Some code to analyze
    tracemalloc.start() 
    start_time = time.time() 

    import tkinter
    print(17)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time-start_time, current, peak

# Example usage
n = 10000

execution_time, current_memory, peak_memory = example_function(n)
print(f"Execution time: {execution_time} seconds")
print(f"Current memory usage: {current_memory/1024} KB")
print(f"Peak memory usage: {peak_memory / 1024} KB")
