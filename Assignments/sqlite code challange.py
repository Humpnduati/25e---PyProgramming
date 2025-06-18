import sqlite3

# Connect to SQLite database (creates company.db if it doesn't exist)
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Create departments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Create employees table with foreign key
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
''')

# Insert sample departments
cursor.executemany('INSERT INTO departments (name) VALUES (?)', [
    ('Engineering',),
    ('Marketing',),
    ('Sales',)
])

# Insert sample employees
cursor.executemany('INSERT INTO employees (name, department_id) VALUES (?, ?)', [
    ('Nduati Githu', 1),
    ('John Mutiso', 1),
    ('Beryl Atieno', 2),
    ('Teresa Juma', 3),
    ('Ethan Davis', 2)
])

# READ: Get all employees with department names
cursor.execute('''
SELECT e.id, e.name, d.name AS department 
FROM employees e 
JOIN departments d ON e.department_id = d.id
''')
for row in cursor.fetchall():
    print(row)

# UPDATE: Change an employee's department (Alice Johnson to Sales)
cursor.execute('''
UPDATE employees 
SET department_id = (SELECT id FROM departments WHERE name = 'Sales')
WHERE name = 'Alice Johnson'
''')

# DELETE: Remove an employee (Bob Smith)
cursor.execute('''
DELETE FROM employees 
WHERE name = 'John Mutiso'
''')

conn.commit()
conn.close()