from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'pavan'

# Configure MySQL connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="pavan",
    database="employee_management"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Create employees table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS employees (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), age INT, experience INT, salary FLOAT, skills VARCHAR(255), qualifications VARCHAR(255))")

# Create users table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARCHAR(255))")


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' in session:
        if request.method == 'POST':
            # Get search query and search criteria from form data
            search_query = request.form['search_query']
            search_criteria = request.form['search_criteria']

            # Construct the SQL query based on the selected search criteria
            query = "SELECT id, first_name, last_name, age, experience, salary, skills, qualifications FROM employees WHERE"
            parameters = []

            if search_criteria == 'name':
                query += " first_name LIKE %s OR last_name LIKE %s"
                parameters.extend(['%' + search_query + '%', '%' + search_query + '%'])                              #.extend() method is to add multiple elements to a line in one go
            elif search_criteria == 'experience':
                query += " experience >= %s"
                parameters.append(search_query)
            elif search_criteria == 'skills':
                query += " skills LIKE %s"
                parameters.append('%' + search_query + '%')
            elif search_criteria == 'salary':
                query += " salary >= %s"
                parameters.append(search_query)

            query += " ORDER BY first_name ASC"

            # Execute the SQL query with the provided parameters
            cursor.execute(query, parameters)
            employees = cursor.fetchall()
            return render_template('index.html', employees=employees, search_query=search_query, search_criteria=search_criteria)

        # Fetch all employees from the database
        cursor.execute("SELECT id, first_name, last_name, age, experience, salary, skills, qualifications FROM employees ORDER BY id ASC")
        employees = cursor.fetchall()
        return render_template('index.html', employees=employees)

    else:
        return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            # Set the user session
            session['user'] = user[0]
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if 'user' in session:
        if request.method == 'POST':
            # Get form data
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = request.form['age']
            experience = request.form['experience']
            salary = request.form['salary']
            skills = request.form['skills']
            qualifications = request.form['qualifications']

            # Insert the new employee into the database
            cursor.execute("INSERT INTO employees (first_name, last_name, age, experience, salary, skills, qualifications) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (first_name, last_name, age, experience, salary, skills, qualifications))
            db.commit()

            return redirect(url_for('index'))

        return render_template('add.html')
    else:
        return redirect(url_for('login'))


@app.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    if 'user' in session:
        if request.method == 'POST':
            # Get form data
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = request.form['age']
            experience = request.form['experience']
            salary = request.form['salary']
            skills = request.form['skills']
            qualifications = request.form['qualifications']

            # Update the employee record in the database
            cursor.execute(
                "UPDATE employees SET first_name=%s, last_name=%s, age=%s, experience=%s, salary=%s, skills=%s, qualifications=%s WHERE id=%s",
                (first_name, last_name, age, experience, salary, skills, qualifications, employee_id))
            db.commit()

            return redirect(url_for('index'))

        # Fetch the employee record from the database
        cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
        employee = cursor.fetchone()
        return render_template('edit.html', employee=employee)
    else:
        return redirect(url_for('login'))


@app.route('/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    if 'user' in session:
        # Delete the employee record from the database
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        db.commit()

    return redirect(url_for('index'))


"""@app.route('/search', methods=['GET', 'POST'])
def search_employee():
    if 'user' in session:
        if request.method == 'POST':
            # Get search query from form data
            search_query = request.form['search_query']

            # Search for employees by name in ascending order
            cursor.execute(
                "SELECT * FROM employees WHERE first_name LIKE %s OR last_name LIKE %s ORDER BY first_name ASC",
                ('%' + search_query + '%', '%' + search_query + '%'))
            employees = cursor.fetchall()
            return render_template('search.html', employees=employees)

        return render_template('search.html')
    else:
        return redirect(url_for('login'))"""


if __name__ == '__main__':
    app.run(debug=True)
