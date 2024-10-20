# db_setup.py
import sqlite3


def create_connection():
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("employees.db")  # Create 'employees.db' file
    return connection


def create_table():
    # Create 'employees' table
    connection = create_connection()
    cursor = connection.cursor()

    # SQL command to create the table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL,
        hire_date TEXT NOT NULL
    )
    ''')

    connection.commit()  # Save (commit) the changes
    connection.close()   # Close the connection


def insert_employee(first_name, last_name, department, salary, hire_date):
    # Insert new employee into the database
    connection = create_connection()
    cursor = connection.cursor()

    # SQL command to insert a new record
    cursor.execute('''
    INSERT INTO employees (first_name, last_name, department, salary, hire_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, department, salary, hire_date))

    connection.commit()  # Save changes
    connection.close()   # Close the connection


def fetch_all_employees():
    # Retrieve all employees from the database
    connection = create_connection()
    cursor = connection.cursor()

    # SQL command to retrieve all records
    cursor.execute('SELECT * FROM employees')

    # Fetch all results as a list of tuples
    employees = cursor.fetchall()

    connection.close()  # Close the connection
    return employees


def update_employee(employee_id, first_name, last_name, department, salary, hire_date):
    # Update an employee's details
    connection = create_connection()
    cursor = connection.cursor()

    # SQL command to update the employee record
    cursor.execute('''
    UPDATE employees
    SET first_name = ?, last_name = ?, department = ?, salary = ?, hire_date = ?
    WHERE employee_id = ?
    ''', (first_name, last_name, department, salary, hire_date, employee_id))

    connection.commit()  # Save changes
    connection.close()   # Close the connection


def delete_employee(employee_id):
    # Delete an employee from the database
    connection = create_connection()
    cursor = connection.cursor()

    # SQL command to delete the employee record
    cursor.execute('''
    DELETE FROM employees
    WHERE employee_id = ?
    ''', (employee_id,))

    connection.commit()  # Save changes
    connection.close()   # Close the connection


# Run the function to create the table
if __name__ == "__main__":
    create_table()
    print("Database and 'employees' table created successfully.")
