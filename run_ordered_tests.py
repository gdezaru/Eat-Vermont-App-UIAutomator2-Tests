import subprocess
import glob
import os
import re

def natural_sort_key(s):
    """Sort strings containing numbers in natural order."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def run_ordered_smoke_tests():
    # Get all test files that start with a number and end with .py
    test_files = glob.glob("[0-9]*_tests_*.py")
    
    # Sort files naturally so that 2 comes after 1, not 10
    test_files.sort(key=natural_sort_key)
    
    # Construct pytest command
    command = ["pytest", "-v", "-m", "smoke"] + test_files
    
    print("Running tests in the following order:")
    for file in test_files:
        print(f"- {file}")
    
    # Run pytest with the ordered files
    subprocess.run(command)

if __name__ == "__main__":
    run_ordered_smoke_tests()
