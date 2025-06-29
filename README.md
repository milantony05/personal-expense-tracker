# Personal Expense Tracker

A Python mini-project to help users log daily expenses, view summaries, and track their spending habits over time. This project demonstrates the use of data structures, file handling, and basic data analysis in Python.

## Objective

Create a Personal Expense Tracker that allows users to:
- Add expenses under different categories
- View summaries of total and categorized spending
- Persist data between runs using file storage

## Features

- **Add Expense:**  
  Log new expenses by specifying amount, category (e.g., Food, Transport), and date (auto or manual). Each entry is stored in a structured format.

- **View Summary:**  
  - See total spending overall
  - View spending by category
  - Analyze spending over time (daily, weekly, or monthly summaries)

- **Data Persistence:**  
  - All expenses are saved to a file (CSV or JSON) for future access
  - Data is automatically loaded on program start

- **User Menu:**  
  - Simple menu to add expenses, view summaries, or exit

- **Bonus (Optional):**  
  - Edit or delete existing expenses
  - Graphical summaries using matplotlib (if implemented)

## How It Works

1. **Adding Expenses:**  
   Enter the amount, category, and date when prompted. The program validates inputs and stores each expense.

2. **Viewing Summaries:**  
   Choose to view overall spending, by category, or over time. The program calculates and displays the results.

3. **Data Storage:**  
   Expenses are saved to a file (for example, `expenses.json` or `expenses.csv`). On startup, the program loads previous records.

4. **Menu Navigation:**  
   Use the menu to add expenses, view summaries, or exit the application.

## Usage

1. Run the program:
`python personal_expense_tracker.py`

2. Follow the menu prompts to add expenses or view summaries.

3. Your data is automatically saved and loaded between sessions.

## Code Structure

- Uses functions for:
- Adding expenses
- Viewing summaries
- File operations (save/load)
- Clean, modular code with comments for clarity

## Instructions

- Ensure Python is installed on your system.
- Place the script and data file in the same directory.
- Run the script and follow on-screen instructions.

## Deliverables

- Python source file (`personal_expense_tracker.py`)
- Data file (`expenses.json` or `expenses.csv`)
- README file (this document)

## License

This project is for educational purposes.
