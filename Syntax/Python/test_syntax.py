# __________Testing (using Pytest)__________
# Pytest is a testing framework for Python. Install it from the terminal using: 
#    pip install pytest
# Test files should start or end with "test".

import pytest
from syntax import add

# The test function should start with "test_".
def test_add():
    # Use the assert keyword to assert that a certain expression is true:
    assert add(1, 2) == 3
    assert add(1, 2, 3) == 6


# A fixture in Pytest is a function used to set up a consistent test environment.
# auto use = True means that this function will automatically be run by pytest before the test.
# scope = "session" means that the function is run once per session, not once per testcase.
@pytest.fixture(scope="session", autouse=True)
def setup(): 
    print("Setup")


# To run all tests, use the command: pytest
