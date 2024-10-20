# main.py
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ttkbootstrap as ttkb
from db_setup import insert_employee, fetch_all_employees, update_employee, delete_employee


def validate_inputs(first_name, last_name, department, salary, hire_date):
    """Validates the form inputs and returns True if valid, False otherwise."""

    # Check if any field is empty
    if not all([first_name, last_name, department, salary, hire_date]):
        messagebox.showerror("Input Error", "All fields are required.")
        return False

    # Validate salary (must be a positive number)
    try:
        salary = float(salary)
        if salary <= 0:
            messagebox.showerror(
                "Input Error", "Salary must be a positive number.")
            return False
    except ValueError:
        messagebox.showerror("Input Error", "Salary must be a valid number.")
        return False

    # Validate hire date (format: YYYY-MM-DD)
    if not re.match(r"\d{4}-\d{2}-\d{2}", hire_date):
        messagebox.showerror(
            "Input Error", "Hire date must be in the format YYYY-MM-DD.")
        return False

    return True


def load_employees():
    """Fetch all employee records and display them in the Treeview."""
    for record in employee_table.get_children():  # Clear existing data
        employee_table.delete(record)

    employees = fetch_all_employees()  # Fetch from the database

    # Insert fetched data into the Treeview
    for employee in employees:
        employee_table.insert("", "end", values=employee)


def add_employee():
    """Insert a new employee into the database and refresh the Treeview."""
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    department = department_entry.get()
    salary = salary_entry.get()
    hire_date = hire_date_entry.get()

    # Validate inputs before inserting into the database
    if validate_inputs(first_name, last_name, department, salary, hire_date):
        insert_employee(first_name, last_name, department, salary, hire_date)
        load_employees()  # Refresh the Treeview
        messagebox.showinfo("Success", "Employee added successfully.")


def select_employee(event):
    """Populate form fields when an employee record is selected from the Treeview."""
    selected = employee_table.focus()
    values = employee_table.item(selected, 'values')

    if values:
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        department_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)
        hire_date_entry.delete(0, tk.END)

        first_name_entry.insert(0, values[1])
        last_name_entry.insert(0, values[2])
        department_entry.insert(0, values[3])
        salary_entry.insert(0, values[4])
        hire_date_entry.insert(0, values[5])


def update_employee_record():
    """Update an existing employee record in the database."""
    selected = employee_table.focus()
    values = employee_table.item(selected, 'values')

    if values:  # Ensure a record is selected
        employee_id = values[0]
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        department = department_entry.get()
        salary = salary_entry.get()
        hire_date = hire_date_entry.get()

        # Validate inputs before updating the database
        if validate_inputs(first_name, last_name, department, salary, hire_date):
            update_employee(employee_id, first_name, last_name,
                            department, salary, hire_date)
            load_employees()  # Refresh the Treeview
            messagebox.showinfo("Success", "Employee updated successfully.")


def delete_employee_record():
    """Delete an employee record from the database."""
    selected = employee_table.focus()
    values = employee_table.item(selected, 'values')

    if values:  # Ensure a record is selected
        employee_id = values[0]
        delete_employee(employee_id)
        load_employees()  # Refresh the Treeview


# Create the main application window
# 'darkly' is one of ttkbootstrap's themes
app = ttkb.Window(themename="darkly")
app.title("Employee Management System")
app.geometry("1250x600")  # Set the window size


# Labels and Entry fields for employee details
ttk.Label(app, text="First Name").grid(row=0, column=0, padx=10, pady=10)
first_name_entry = ttk.Entry(app)
first_name_entry.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(app, text="Last Name").grid(row=1, column=0, padx=10, pady=10)
last_name_entry = ttk.Entry(app)
last_name_entry.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(app, text="Department").grid(row=2, column=0, padx=10, pady=10)
department_entry = ttk.Entry(app)
department_entry.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(app, text="Salary").grid(row=3, column=0, padx=10, pady=10)
salary_entry = ttk.Entry(app)
salary_entry.grid(row=3, column=1, padx=10, pady=10)

ttk.Label(app, text="Hire Date (YYYY-MM-DD)").grid(row=4,
                                                   column=0, padx=10, pady=10)
hire_date_entry = ttk.Entry(app)
hire_date_entry.grid(row=4, column=1, padx=10, pady=10)


# Buttons for Add, Update, and Delete
ttk.Button(app, text="Add Employee", command=lambda: add_employee()
           ).grid(row=5, column=0, padx=10, pady=10)
ttk.Button(app, text="Update Employee", command=lambda: update_employee_record(
)).grid(row=5, column=1, padx=10, pady=10)
ttk.Button(app, text="Delete Employee", command=lambda: delete_employee_record(
)).grid(row=5, column=2, padx=10, pady=10)


# Treeview to display employee records
columns = ("ID", "First Name", "Last Name",
           "Department", "Salary", "Hire Date")
employee_table = ttk.Treeview(app, columns=columns, show="headings")

# Define column headers
for col in columns:
    employee_table.heading(col, text=col)

employee_table.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Scrollbar for the Treeview
scrollbar = ttk.Scrollbar(app, orient="vertical", command=employee_table.yview)
employee_table.configure(yscroll=scrollbar.set)
scrollbar.grid(row=6, column=3, sticky="ns", pady=10)

# Triggered when a row is clicked
employee_table.bind("<ButtonRelease-1>", select_employee)

# Load employees on startup
load_employees()


# Run the application
app.mainloop()
