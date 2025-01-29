from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database Configuration
db_user = 
db_password = 
db_host = 
db_port = 
db_name = 

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )

# Homepage Route
@app.route('/')
def index():
    return render_template('index.html')

# 3.1 Add a new USER_ACCOUNT
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data = request.form
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """
            INSERT INTO USER_ACCOUNT (Id_No, F_Name, Phone, Role_Name)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (data['id_no'], data['f_name'], data['phone'], data['role_name']))
            connection.commit()
            return redirect('/')
        except mysql.connector.Error as error:
            return f"Error: {error}"
        finally:
            cursor.close()
            connection.close()
    return render_template('add_user.html')

# 3.2 Add a new ROLE
@app.route('/add_role', methods=['GET', 'POST'])
def add_role():
    if request.method == 'POST':
        data = request.form
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """
            INSERT INTO USER_ROLE (Role_Name, Description)
            VALUES (%s, %s)
            """
            cursor.execute(sql, (data['role_name'], data['description']))
            connection.commit()
            return redirect('/')
        except mysql.connector.Error as error:
            return f"Error: {error}"
        finally:
            cursor.close()
            connection.close()
    return render_template('add_role.html')

# 3.3 Add a new TABLE
@app.route('/add_table', methods=['GET', 'POST'])
def add_table():
    if request.method == 'POST':
        data = request.form
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """
            INSERT INTO `TABLE` (Table_Name, Owner_Id)
            VALUES (%s, %s)
            """
            cursor.execute(sql, (data['table_name'], data['owner_id']))
            connection.commit()
            return redirect('/')
        except mysql.connector.Error as error:
            return f"Error: {error}"
        finally:
            cursor.close()
            connection.close()
    return render_template('add_table.html')

# 3.4 Add a new PRIVILEGE
@app.route('/add_privilege', methods=['GET', 'POST'])
def add_privilege():
    if request.method == 'POST':
        data = request.form
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """
            INSERT INTO PRIVILEGE (Privilege_Name)
            VALUES (%s)
            """
            cursor.execute(sql, (data['privilege_name'],))
            privilege_type = data['privilege_type'].lower()
            if privilege_type == 'account':
                child_sql = "INSERT INTO ACCOUNT_PRIVILEGE (Privilege_Name) VALUES (%s)"
            elif privilege_type == 'relation':
                child_sql = "INSERT INTO RELATIONAL_PRIVILEGE (Privilege_Name) VALUES (%s)"
            else:
                raise ValueError("Invalid privilege type!")
            cursor.execute(child_sql, (data['privilege_name'],))
            connection.commit()
            return redirect('/')
        except mysql.connector.Error as error:
            return f"Error: {error}"
        finally:
            cursor.close()
            connection.close()
    return render_template('add_privilege.html')

# 3.5 Relate a USER_ACCOUNT to a ROLE
@app.route('/relate_user_role', methods=['GET', 'POST'])
def relate_user_role():
    if request.method == 'POST':
        data = request.form
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """
            UPDATE USER_ACCOUNT
            SET Role_Name = %s
            WHERE Id_No = %s
            """
            cursor.execute(sql, (data['role_name'], data['id_no']))
            connection.commit()
            return redirect('/')
        except mysql.connector.Error as error:
            return f"Error: {error}"
        finally:
            cursor.close()
            connection.close()
    return render_template('relate_user_role.html')

# 3.6 Relate an ACCOUNT_PRIVILEGE to a ROLE
@app.route('/relate_account_privilege', methods=['GET', 'POST'])
def relate_account_privilege():
    if request.method == 'POST':
        data = request.form
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """
            INSERT INTO ACCOUNT_PRIVILEGE_GRANTED (Privilege_Name, Role_Name)
            VALUES (%s, %s)
            """
            cursor.execute(sql, (data['privilege_name'], data['role_name']))
            connection.commit()
            return redirect('/')
        except mysql.connector.Error as error:
            return f"Error: {error}"
        finally:
            cursor.close()
            connection.close()
    return render_template('relate_account_privilege.html')

# 3.7 Relate a RELATION_PRIVILEGE to a TABLE
@app.route('/relate_relation_privilege', methods=['GET', 'POST'])
def relate_relation_privilege():
    if request.method == 'POST':
        data = request.form
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """
            INSERT INTO ASSIGNED_TABLE_PRIVILEGE (Table_Name, Role_Name, Privilege_Name)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (data['table_name'], data['role_name'], data['privilege_name']))
            connection.commit()
            return redirect('/')
        except mysql.connector.Error as error:
            return f"Error: {error}"
        finally:
            cursor.close()
            connection.close()
    return render_template('relate_relation_privilege.html')

# 3.8 Retrieve privileges
@app.route('/retrieve_privileges', methods=['GET', 'POST'])
def retrieve_privileges():
    if request.method == 'POST':
        data = request.form
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            if data['type'] == 'user':
                sql = """
                SELECT DISTINCT Privilege_Name
                FROM USER_ACCOUNT UA
                JOIN ACCOUNT_PRIVILEGE_GRANTED APG ON UA.Role_Name = APG.Role_Name
                WHERE UA.Id_No = %s
                """
                cursor.execute(sql, (data['id_or_role'],))
            else:
                sql = """
                SELECT Privilege_Name
                FROM ACCOUNT_PRIVILEGE_GRANTED
                WHERE Role_Name = %s
                """
                cursor.execute(sql, (data['id_or_role'],))
            privileges = cursor.fetchall()
            return render_template('retrieve_privileges.html', privileges=privileges)
        except mysql.connector.Error as error:
            return f"Error: {error}"
        finally:
            cursor.close()
            connection.close()
    return render_template('retrieve_privileges.html', privileges=None)

if __name__ == '__main__':
    app.run(debug=True)
