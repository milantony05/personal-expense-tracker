import json
import csv
from datetime import datetime, timedelta
import os

class PersonalExpenseTracker:
    def __init__(self, data_file="expenses.json"):
        """Initialize the expense tracker with data file."""
        self.data_file = data_file
        self.expenses = []
        self.categories = ["Food", "Transport", "Entertainment", "Utilities", 
                          "Healthcare", "Shopping", "Education", "Other"]
        self.load_expenses()

    def load_expenses(self):
        """Load expenses from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.expenses = json.load(file)
                print(f"Loaded {len(self.expenses)} expenses from {self.data_file}")
            else:
                print("No existing expense data found. Starting fresh!")
        except Exception as e:
            print(f"Error loading expenses: {e}")
            self.expenses = []

    def save_expenses(self):
        """Save expenses to JSON file."""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.expenses, file, indent=2)
            print("Expenses saved successfully!")
        except Exception as e:
            print(f"Error saving expenses: {e}")

    def add_expense(self):
        """Add a new expense to the tracker."""
        print("\n--- Add New Expense ---")

        # Get amount
        while True:
            try:
                amount = float(input("Enter amount: "))
                if amount <= 0:
                    print("Amount must be positive. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        # Get category
        print("\nAvailable categories:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")

        while True:
            try:
                choice = input("\nSelect category (number or name): ").strip()
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(self.categories):
                        category = self.categories[choice_num - 1]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                elif choice in self.categories:
                    category = choice
                    break
                else:
                    print("Invalid category. Please try again.")
            except ValueError:
                print("Please enter a valid choice.")

        # Get date
        while True:
            date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date_input:
                date = datetime.now().strftime("%Y-%m-%d")
                break
            else:
                try:
                    datetime.strptime(date_input, "%Y-%m-%d")
                    date = date_input
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")

        # Get description (optional)
        description = input("Enter description (optional): ").strip()

        # Create expense record
        expense = {
            "id": len(self.expenses) + 1,
            "amount": amount,
            "category": category,
            "date": date,
            "description": description,
            "created_at": datetime.now().isoformat()
        }

        self.expenses.append(expense)
        self.save_expenses()
        print(f"\nExpense added successfully!")
        print(f"Amount: {amount:.2f}")
        print(f"Category: {category}")
        print(f"Date: {date}")
        if description:
            print(f"Description: {description}")

    def view_all_expenses(self):
        """Display all expenses."""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return

        print("\n--- All Expenses ---")
        print(f"{'ID':<4} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description':<20}")
        print("-" * 65)

        for expense in self.expenses:
            desc = expense.get('description', '')[:18] + '...' if len(expense.get('description', '')) > 20 else expense.get('description', '')
            print(f"{expense['id']:<4} {expense['date']:<12} {expense['category']:<15} {expense['amount']:<9.2f} {desc:<20}")

    def view_summary(self):
        """Display expense summaries."""
        if not self.expenses:
            print("\nNo expenses to summarize.")
            return

        print("\n--- Expense Summary ---")

        # Total spending
        total = sum(expense['amount'] for expense in self.expenses)
        print(f"Total Overall Spending: {total:.2f}")

        # Category-wise spending
        category_totals = {}
        for expense in self.expenses:
            category = expense['category']
            category_totals[category] = category_totals.get(category, 0) + expense['amount']

        print("\nSpending by Category:")
        print(f"{'Category':<15} {'Amount':<10} {'Percentage':<10}")
        print("-" * 35)

        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100
            print(f"{category:<15} {amount:<9.2f} {percentage:<9.1f}%")

        # Recent expenses (last 7 days)
        recent_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        recent_expenses = [exp for exp in self.expenses if exp['date'] >= recent_date]
        recent_total = sum(exp['amount'] for exp in recent_expenses)

        print(f"\nLast 7 Days Spending: {recent_total:.2f}")
        print(f"Average Daily Spending: {recent_total/7:.2f}")

    def view_category_summary(self):
        """View summary for a specific category."""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return

        print("\nAvailable categories:")
        categories_with_expenses = set(exp['category'] for exp in self.expenses)

        for i, category in enumerate(sorted(categories_with_expenses), 1):
            print(f"{i}. {category}")

        category = input("\nEnter category name: ").strip()

        if category not in categories_with_expenses:
            print("No expenses found for this category.")
            return

        category_expenses = [exp for exp in self.expenses if exp['category'] == category]
        total = sum(exp['amount'] for exp in category_expenses)

        print(f"\n--- {category} Summary ---")
        print(f"Total Expenses: {len(category_expenses)}")
        print(f"Total Amount: {total:.2f}")
        print(f"Average per expense: {total/len(category_expenses):.2f}")

        print("\nRecent expenses in this category:")
        for expense in sorted(category_expenses, key=lambda x: x['date'], reverse=True)[:5]:
            print(f"  {expense['date']}: {expense['amount']:.2f} - {expense.get('description', 'No description')}")

    def delete_expense(self):
        """Delete an expense by ID."""
        if not self.expenses:
            print("\nNo expenses to delete.")
            return

        self.view_all_expenses()

        try:
            expense_id = int(input("\nEnter the ID of the expense to delete: "))

            # Find expense by ID
            for i, expense in enumerate(self.expenses):
                if expense['id'] == expense_id:
                    deleted_expense = self.expenses.pop(i)
                    self.save_expenses()
                    print(f"\nDeleted expense: {deleted_expense['amount']:.2f} - {deleted_expense['category']} on {deleted_expense['date']}")
                    return

            print("Expense not found.")
        except ValueError:
            print("Please enter a valid ID number.")

    def edit_expense(self):
        """Edit an existing expense."""
        if not self.expenses:
            print("\nNo expenses to edit.")
            return

        self.view_all_expenses()

        try:
            expense_id = int(input("\nEnter the ID of the expense to edit: "))

            # Find expense by ID
            expense_to_edit = None
            for expense in self.expenses:
                if expense['id'] == expense_id:
                    expense_to_edit = expense
                    break

            if not expense_to_edit:
                print("Expense not found.")
                return

            print(f"\nEditing expense: {expense_to_edit['amount']:.2f} - {expense_to_edit['category']} on {expense_to_edit['date']}")

            # Edit amount
            new_amount = input(f"New amount (current: {expense_to_edit['amount']:.2f}): ").strip()
            if new_amount:
                try:
                    expense_to_edit['amount'] = float(new_amount)
                except ValueError:
                    print("Invalid amount, keeping original.")

            # Edit category
            print("\nAvailable categories:")
            for i, category in enumerate(self.categories, 1):
                print(f"{i}. {category}")

            new_category = input(f"New category (current: {expense_to_edit['category']}): ").strip()
            if new_category and new_category in self.categories:
                expense_to_edit['category'] = new_category

            # Edit date
            new_date = input(f"New date (current: {expense_to_edit['date']}): ").strip()
            if new_date:
                try:
                    datetime.strptime(new_date, "%Y-%m-%d")
                    expense_to_edit['date'] = new_date
                except ValueError:
                    print("Invalid date format, keeping original.")

            # Edit description
            new_description = input(f"New description (current: {expense_to_edit.get('description', 'None')}): ").strip()
            if new_description:
                expense_to_edit['description'] = new_description

            self.save_expenses()
            print("\nExpense updated successfully!")

        except ValueError:
            print("Please enter a valid ID number.")

    def export_to_csv(self):
        """Export expenses to CSV file."""
        if not self.expenses:
            print("\nNo expenses to export.")
            return

        filename = f"expenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['id', 'date', 'category', 'amount', 'description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for expense in self.expenses:
                    writer.writerow({
                        'id': expense['id'],
                        'date': expense['date'],
                        'category': expense['category'],
                        'amount': expense['amount'],
                        'description': expense.get('description', '')
                    })

            print(f"\nExpenses exported to {filename}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("      PERSONAL EXPENSE TRACKER")
        print("="*50)
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Summary")
        print("4. View Category Summary")
        print("5. Edit Expense")
        print("6. Delete Expense")
        print("7. Export to CSV")
        print("8. Exit")
        print("="*50)

    def run(self):
        """Main program loop."""
        print("Welcome to Personal Expense Tracker!")

        while True:
            self.display_menu()

            try:
                choice = input("\nSelect an option (1-8): ").strip()

                if choice == '1':
                    self.add_expense()
                elif choice == '2':
                    self.view_all_expenses()
                elif choice == '3':
                    self.view_summary()
                elif choice == '4':
                    self.view_category_summary()
                elif choice == '5':
                    self.edit_expense()
                elif choice == '6':
                    self.delete_expense()
                elif choice == '7':
                    self.export_to_csv()
                elif choice == '8':
                    print("\nThank you for using Personal Expense Tracker!")
                    print("Your expenses have been saved.")
                    break
                else:
                    print("\nInvalid choice. Please select 1-8.")

                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\nProgram interrupted. Saving data...")
                self.save_expenses()
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")

def main():
    """Main function to run the expense tracker."""
    tracker = PersonalExpenseTracker()
    tracker.run()

if __name__ == "__main__":
    main()
