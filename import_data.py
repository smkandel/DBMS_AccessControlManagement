import mysql.connector

# Connect to the database
db_user = 
db_password = 
db_host = 
db_port =  
db_name = 




# Construct the MySQL connection string
conn_str = {
    'user': db_user,
    'password': db_password,
    'host': db_host,
    'port': db_port,
    'database': db_name
}

try:
    # Connect to the database
    db = mysql.connector.connect(**conn_str)
    cursor = db.cursor()

    # Insert data into PRIVILEGE table
    privileges = [
        ("SELECT",), ("INSERT",), ("DELETE",), ("UPDATE",), ("CREATETABLE",), ("DROPTABLE",)
    ]
    cursor.executemany("INSERT INTO PRIVILEGE (Privilege_Name) VALUES (%s)", privileges)

    # Insert data into ACCOUNT_PRIVILEGE table
    account_privileges = [("CREATETABLE",), ("DROPTABLE",)]
    cursor.executemany("INSERT INTO ACCOUNT_PRIVILEGE (Privilege_Name) VALUES (%s)", account_privileges)

    # Insert data into RELATIONAL_PRIVILEGE table
    relational_privileges = [("SELECT",), ("INSERT",), ("DELETE",), ("UPDATE",)]
    cursor.executemany("INSERT INTO RELATIONAL_PRIVILEGE (Privilege_Name) VALUES (%s)", relational_privileges)

    # Insert data into USER_ROLE table
    roles = [
        ("Admin", "Has all privileges"),
        ("Developer", "Can create and modify data"),
        ("Analyst", "Can read and analyze data")
    ]
    cursor.executemany("INSERT INTO USER_ROLE (Role_Name, Description) VALUES (%s, %s)", roles)

    # Insert data into USER_ACCOUNT table
    user_accounts = [
        (1, "J.Smith", "817-272-3000", "Admin"),
        (2, "R.Wong", "817-272-4000", "Developer"),
        (3, "A.Patel", "817-272-5000", "Analyst"),
        (4, "K.Tan", "817-272-6000", "Developer"),
        (5, "M.Lee", "817-272-7000", "Analyst"),
        (6, "S.Kumar", "817-272-8000", "Developer"),
        (7, "C.Martinez", "817-272-9000", "Analyst"),
        (8, "L.Perez", "817-272-1000", "Admin"),
        (9, "D.Lopez", "817-272-1100", "Developer"),
        (10, "B.Garcia", "817-272-1200", "Analyst")
    ]
    cursor.executemany("INSERT INTO USER_ACCOUNT (Id_No, F_Name, Phone, Role_Name) VALUES (%s, %s, %s, %s)", user_accounts)

    # Insert data into TABLE table
    tables = [
        ("Sales", 1), ("Orders", 2), ("Products", 3), ("Customers", 4),
        ("Employees", 5), ("Inventory", 6), ("Payments", 7), ("Shipments", 8),
        ("Suppliers", 9), ("Reports", 10)
    ]
    cursor.executemany("INSERT INTO `TABLE` (Table_Name, Owner_Id) VALUES (%s, %s)", tables)

    # Insert data into ACCOUNT_PRIVILEGE_GRANTED table
    account_privilege_granted = [
        ("CREATETABLE", "Admin"),
        ("DROPTABLE", "Admin"),
        ("CREATETABLE", "Developer")
    ]
    cursor.executemany("INSERT INTO ACCOUNT_PRIVILEGE_GRANTED (Privilege_Name, Role_Name) VALUES (%s, %s)", account_privilege_granted)

    # Insert data into ASSIGNED_TABLE_PRIVILEGE table
    assigned_table_privilege = [
        ("Sales", "Admin", "SELECT"), ("Orders", "Developer", "INSERT"),
        ("Products", "Analyst", "SELECT"), ("Customers", "Admin", "DELETE"),
        ("Employees", "Developer", "UPDATE"), ("Inventory", "Analyst", "SELECT"),
        ("Payments", "Admin", "SELECT"), ("Shipments", "Developer", "INSERT"),
        ("Suppliers", "Analyst", "SELECT"), ("Reports", "Admin", "UPDATE")
    ]
    cursor.executemany("INSERT INTO ASSIGNED_TABLE_PRIVILEGE (Table_Name, Role_Name, Privilege_Name) VALUES (%s, %s, %s)", assigned_table_privilege)

    # Commit changes to the database
    db.commit()
    print("Data loaded successfully!")

except mysql.connector.Error as error:
    print("Error executing transactions:", error)

finally:
    # Close the cursor and connection
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'db' in locals() and db:
        db.close()