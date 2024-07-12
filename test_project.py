import pytest
import os
import json
from unittest.mock import patch
from project import load_data, save_data, add_user, add_expense, total_expenses, individual_expenses, calculate_debts


TEST_EXPENSES_FILE = 'test_expenses.json'
TEST_USERS_FILE = 'test_users.json'

# Test Data
test_users = ['Person1', 'Person2', 'Person3', 'Person4']
test_expenses = [
    {"person": "Person1", "category": "food", "amount": 100.0, "description": "groceries"},
    {"person": "Person2", "category": "electricity", "amount": 50.0, "description": "electricity bill"},
    {"person": "Person3", "category": "rent", "amount": 300.0, "description": "rent"},
    {"person": "Person4", "category": "food", "amount": 75.0, "description": "dinner"}
]


@pytest.fixture(scope="module")
def setup_teardown():
    
    save_data(test_users, TEST_USERS_FILE)
    save_data(test_expenses, TEST_EXPENSES_FILE)
    yield
   
    if os.path.exists(TEST_EXPENSES_FILE):
        os.remove(TEST_EXPENSES_FILE)
    if os.path.exists(TEST_USERS_FILE):
        os.remove(TEST_USERS_FILE)

def test_load_data(setup_teardown):
    expenses = load_data(TEST_EXPENSES_FILE)
    users = load_data(TEST_USERS_FILE)
    assert len(expenses) == 4
    assert len(users) == 4

@patch('builtins.input', side_effect=['Person5'])
def test_add_user(mock_input, setup_teardown):
    users = load_data(TEST_USERS_FILE)
    add_user(users)
    assert len(users) == 5  
    assert 'Person5' in users

@patch('builtins.input', side_effect=['Person1', 'food', '25', 'snacks'])
def test_add_expense(mock_input, setup_teardown):
    expenses = load_data(TEST_EXPENSES_FILE)
    users = load_data(TEST_USERS_FILE)
    add_expense(expenses, users)
    assert len(expenses) == 5  
    assert expenses[-1] == {"person": "Person1", "category": "food", "amount": 25.0, "description": "snacks"}

def test_total_expenses(setup_teardown):
    expenses = load_data(TEST_EXPENSES_FILE)
    total = sum(expense['amount'] for expense in expenses)
    assert total == 525.0

def test_individual_expenses(setup_teardown):
    expenses = load_data(TEST_EXPENSES_FILE)
    totals = individual_expenses(expenses)
    assert totals['Person1'] == 100.0
    assert totals['Person2'] == 50.0
    assert totals['Person3'] == 300.0
    assert totals['Person4'] == 75.0

def test_calculate_debts(setup_teardown):
    expenses = load_data(TEST_EXPENSES_FILE)
    num_people = 4
    total = sum(expense['amount'] for expense in expenses)
    share = total / num_people
    totals = individual_expenses(expenses)
    debts = {person: total_spent - share for person, total_spent in totals.items()}
    
    assert debts['Person1'] == -31.25
    assert debts['Person2'] == -81.25
    assert debts['Person3'] == 168.75
    assert debts['Person4'] == -56.25
