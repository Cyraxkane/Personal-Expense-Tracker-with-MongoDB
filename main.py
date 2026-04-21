import sys
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

class Expense:
    """
    A class to represent a data model individual expense entry for application.
    """
    def __init__(self, description, amount, date):
        self.description = description
        self.amount = amount
        self.date = date

    def to_dict(self):
        """
        Converts the expense object properties into a dictionary.
        """
        return {
            "description": self.description,
            "amount": self.amount,
            "date": self.date
        }

class ExpenseTracker:
    """
    The main controller class that handles MongoDB connections 
    and CRUD operations.
    """
    def __init__(self, uri="mongodb://localhost:27017/", db_name="ExpenseTracker"):
        """Initializes the MongoDB client and tests the connection."""
        try:
            # Establishing connection to the MongoDB instance
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            self.collection = self.db.expenses
            # The 'ping' command is used to verify the server is reachable
            self.client.admin.command('ping')
        except Exception as e:
            print(f"Error: Could not connect to MongoDB. Ensure the service is running.")
            print(f"Details: {e}")
            sys.exit(1)

    def add_expense(self):
        """Prompts user for input, validates data, and saves to MongoDB."""
        print("\n--- Add New Expense ---")
        
        description = input("Enter description: ").strip()
        if not description:
            print("Description cannot be empty.")
            return

        amount = None
        while amount is None:
            try:
                raw_amount = float(input("Enter amount: "))
                if raw_amount > 0:
                    amount = raw_amount
                else:
                    print("Error: Amount must be a positive number.")
                    main_menu()
            except ValueError:
                print("Error: Invalid input. Please enter a numeric value (e.g., 10.50).")
                main_menu()

        date_str = None
        while date_str is None:
            raw_date = input("Enter date (YYYY-MM-DD): ").strip()
            try:
                # Validates string against specific format
                datetime.strptime(raw_date, '%Y-%m-%d')
                date_str = raw_date
            except ValueError:
                print("Error: Incorrect format. Please use YYYY-MM-DD.")
                main_menu()

        # Create Expense and insert into MongoDB
        new_expense = Expense(description, amount, date_str)
        self.collection.insert_one(new_expense.to_dict())
        print(f"\nSuccessfully added: {description} (${amount:.2f})")

    def view_all_expenses(self):
        """Fetches all data from the database and prints them."""
        print("\n--- All Recorded Expenses ---")
        expenses = list(self.collection.find())
        
        if not expenses:
            print("No expenses found in the database.")
            return
        
        for exp in expenses:
            print(f"ID: {exp['_id']} | Desc: {exp['description']} | "
                  f"Amount: ${exp['amount']:.2f} | Date: {exp['date']}")

    def view_total_expenses(self):
        """Uses MongoDB Aggregation to sum all expense amounts."""
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        
        # If result is empty, total is 0.0
        total = result[0]['total'] if result else 0.0
        print(f"\nTotal Amount Spent: ${total:.2f}")

    def delete_expense(self):
        """Allows user to delete a specific record using its unique MongoDB ID."""
        self.view_all_expenses()
        expense_id = input("\nEnter the ID of the expense to delete: ").strip()
        
        try:
            # Convert string ID to MongoDB ObjectId
            result = self.collection.delete_one({"_id": ObjectId(expense_id)})
            if result.deleted_count > 0:
                print("Expense deleted successfully.")
            else:
                print("No expense found with that ID.")
                main_menu()
        except InvalidId:
            print("Error: Invalid ID format. Please copy/paste the ID from the list.")
            main_menu()

def main_menu():
    """Provides the user interface and navigation for the application."""
    tracker = ExpenseTracker()
    
    while True:
        print("\n==========================")
        print(" Personal Expense Tracker ")
        print("==========================")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. View Total Expenses")
        print("4. Delete an Expense")
        print("5. Exit")
        
        choice = input("Enter your option: ").strip()
        
        if choice == '1':
            tracker.add_expense()
        elif choice == '2':
            tracker.view_all_expenses()
        elif choice == '3':
            tracker.view_total_expenses()
        elif choice == '4':
            tracker.delete_expense()
        elif choice == '5':
            print("Exiting... Goodbye!")
            # Closes the application completely
            exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    # Script entry point
    main_menu()
