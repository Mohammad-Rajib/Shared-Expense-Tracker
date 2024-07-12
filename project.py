import os
import json
import matplotlib.pyplot as plt

def main():
    expenses = load_data(EXPENSES_JSON_FILE)
    users = load_data(USERS_JSON_FILE)
    
    while True:
        print("\nShared Expense Tracker")
        print("1. Add User")
        print("2. Add Expense")
        print("3. View Expenses")
        print("4. Calculate Total Expenses")
        print("5. Calculate Each Person's Share")
        print("6. Calculate Individual Expenses")
        print("7. Calculate Debts")
        print("8. Generate Expense Report")
        print("9. Delete Expenses File")
        print("10. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_user(users)
        elif choice == '2':
            add_expense(expenses, users)
        elif choice == '3':
            view_expenses(expenses)
        elif choice == '4':
            total_expenses(expenses)
        elif choice == '5':
            calculate_share(expenses, len(users))
        elif choice == '6':
            individual_expenses(expenses)
        elif choice == '7':
            calculate_debts(expenses, len(users))
        elif choice == '8':
            generate_report(expenses)
        elif choice == '9':
            delete_expenses_file()
        elif choice == '10':
            break
        else:
            print("Invalid choice. Please try again.")


EXPENSES_JSON_FILE = 'expenses file.json'
USERS_JSON_FILE = 'users file.json'

def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    return []

def save_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)

def delete_expenses_file():
    if os.path.exists(EXPENSES_JSON_FILE):
        os.remove(EXPENSES_JSON_FILE)
        print(f"{EXPENSES_JSON_FILE} has been deleted.")
    else:
        print(f"{EXPENSES_JSON_FILE} does not exist.")


def add_user(users):
    username = input("Enter username: ")
    users.append(username)
    save_data(users, USERS_JSON_FILE)
    print(f"User {username} added.")

def add_expense(expenses, users):
    if not users:
        print("No users available. Please add users first.")
        return
    
    person = input(f"Enter the person who paid ({', '.join(users)}): ")
    if person not in users:
        print("Invalid user. Please enter a valid user.")
        return
    
    category = input("Enter expense category (food, electricity, rent, etc.): ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")
    expenses.append({"person": person, "category": category, "amount": amount, "description": description})
    save_data(expenses, EXPENSES_JSON_FILE)

def view_expenses(expenses):
    for expense in expenses:
        print(f"Person: {expense['person']}, Category: {expense['category']}, Amount: {expense['amount']}, Description: {expense['description']}")

def total_expenses(expenses):
    total = sum(expense['amount'] for expense in expenses)
    print(f"Total Expenses: {total}")

def calculate_share(expenses, num_people):
    total = sum(expense['amount'] for expense in expenses)
    share = total / num_people
    print(f"Each person should contribute: {share}")

def individual_expenses(expenses):
    totals = {}
    for expense in expenses:
        if 'person' not in expense or 'amount' not in expense:
            print(f"Invalid expense entry: {expense}")
            continue
        if expense['person'] in totals:
            totals[expense['person']] += expense['amount']
        else:
            totals[expense['person']] = expense['amount']
    for person, total in totals.items():
        print(f"{person} has spent: {total}")
    return totals

def calculate_debts(expenses, num_people):
    total = sum(expense['amount'] for expense in expenses)
    share = total / num_people
    totals = individual_expenses(expenses)
    
    for person, total_spent in totals.items():
        debt = total_spent - share
        if debt > 0:
            print(f"{person} is owed {debt}")
        else:
            print(f"{person} owes {-debt}")

def generate_report(expenses):
    categories = {}
    for expense in expenses:
        if expense['category'] in categories:
            categories[expense['category']] += expense['amount']
        else:
            categories[expense['category']] = expense['amount']
    
    categories_list = list(categories.keys())
    values = list(categories.values())

    plt.figure(figsize=(10, 5))
    plt.bar(categories_list, values, color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.title('Expenses by Category')
    plt.show()


if __name__ == "__main__":
    main()
