import mysql.connector

# Connect to the database


# Construct the MySQL connection string
conn_str = {
    'user': db_user,
    'password': db_password,
    'host': db_host,
    'port': db_port,
    'database': db_name
}

# 1 Function to add a new USER_ACCOUNT
def add_user_account(cursor, id_no, f_name, phone, role_name):
    sql = """
    INSERT INTO USER_ACCOUNT (Id_No, F_Name, Phone, Role_Name)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (id_no, f_name, phone, role_name))

# 2 Function to add Add All Information About a New ROLE
def add_role(cursor, role_name, description):
    sql = """
    INSERT INTO USER_ROLE (Role_Name, Description)
    VALUES (%s, %s)
    """
    cursor.execute(sql, (role_name, description))

# 3 Function Add All Information About a New TABLE
def add_table(cursor, table_name, owner_id):
    sql = """
    INSERT INTO `TABLE` (Table_Name, Owner_Id)
    VALUES (%s, %s)
    """
    cursor.execute(sql, (table_name, owner_id))


try:
    # Connect to the database
    db = mysql.connector.connect(**conn_str)
    cursor = db.cursor()

    # Task 3.1: Add a new USER_ACCOUNT
    add_user_account(cursor, 11, "T.Roberts", "817-272-1300", "Analyst")

    # Task 3.2: Add a new ROLE
    add_role(cursor, "Manager", "Manages the operations")

    # Task 3.3: Add a new TABLE
    add_table(cursor, "Projects", 11)

finally:
    # Close the cursor and database connection
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals():
        db.close()

    # Commit all changes
    db.commit()
    print("All transactions executed successfully!")



# 4 Function to Insert a New PRIVILEGE (Including Privilege Type)
def add_privilege(cursor, privilege_name, privilege_type):
    # Insert into the parent PRIVILEGE table first
    parent_sql = """
    INSERT INTO PRIVILEGE (Privilege_Name)
    VALUES (%s)
    """
    try:
        cursor.execute(parent_sql, (privilege_name,))
    except mysql.connector.IntegrityError:
        # If the privilege already exists in the parent table, skip it
        print(f"Privilege '{privilege_name}' already exists in the PRIVILEGE table.")

    # Insert into the appropriate child table (ACCOUNT_PRIVILEGE or RELATIONAL_PRIVILEGE)
    if privilege_type.lower() == "account":
        child_sql = """
        INSERT INTO ACCOUNT_PRIVILEGE (Privilege_Name)
        VALUES (%s)
        """
    elif privilege_type.lower() == "relation":
        child_sql = """
        INSERT INTO RELATIONAL_PRIVILEGE (Privilege_Name)
        VALUES (%s)
        """
    else:
        # Raise a ValueError for invalid privilege types
        raise ValueError("Invalid privilege type. Use 'account' or 'relation'.")

    try:
        cursor.execute(child_sql, (privilege_name,))
    except mysql.connector.IntegrityError:
        # If the privilege already exists in the child table, skip it
        print(f"Privilege '{privilege_name}' already exists in the {privilege_type.upper()} table.")


try:
    # Connect to the database
    db = mysql.connector.connect(**conn_str)
    cursor = db.cursor()

    # Task 3.4: Insert a new PRIVILEGE
    add_privilege(cursor, "EXECUTE", "account")  # Valid privilege type
    add_privilege(cursor, "GRANT", "relation")  # Valid privilege type

    # Commit all changes
    db.commit()
    print("All transactions executed successfully!")

except mysql.connector.Error as error:
    print("Error during transactions:", error)

finally:
    # Close resources
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals():
        db.close()



# #####3.5 Function to Relate a USER_ACCOUNT to a ROLE   #select from user_account to check the upate
def relate_user_to_role(cursor, id_no, role_name):
    """Relate a USER_ACCOUNT to a ROLE with validations."""
    print(f"Relating user ID {id_no} to role '{role_name}'...")

    # Validate if the role exists in USER_ROLE
    validate_role_sql = """
    SELECT Role_Name
    FROM USER_ROLE
    WHERE Role_Name = %s
    """
    cursor.execute(validate_role_sql, (role_name,))
    role = cursor.fetchone()
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist in USER_ROLE. Please add the role first.")
    
    print(f"Role '{role_name}' exists in USER_ROLE.")

    # Validate if the user exists in USER_ACCOUNT
    validate_user_sql = """
    SELECT Id_No
    FROM USER_ACCOUNT
    WHERE Id_No = %s
    """
    cursor.execute(validate_user_sql, (id_no,))
    user = cursor.fetchone()
    if not user:
        raise ValueError(f"No user found with ID {id_no} in USER_ACCOUNT.")
    
    print(f"User with ID {id_no} exists in USER_ACCOUNT.")

    # Update the USER_ACCOUNT with the new role
    update_user_sql = """
    UPDATE USER_ACCOUNT
    SET Role_Name = %s
    WHERE Id_No = %s
    """
    cursor.execute(update_user_sql, (role_name, id_no))
    print(f"Rows affected: {cursor.rowcount}")

    # Check if the update was successful
    if cursor.rowcount == 0:
        raise ValueError(f"Failed to update role for user ID {id_no}.")
    print(f"User ID {id_no} successfully updated to role '{role_name}'.")

def print_user_account(cursor, id_no):
    """Retrieve and print details of a specific user account."""
    sql = """
    SELECT Id_No, F_Name, Phone, Role_Name
    FROM USER_ACCOUNT
    WHERE Id_No = %s
    """
    cursor.execute(sql, (id_no,))
    result = cursor.fetchone()
    if result:
        print(f"Updated User Account Details:\nID: {result[0]}\nName: {result[1]}\nPhone: {result[2]}\nRole: {result[3]}")
    else:
        print(f"No user found with ID {id_no}.")

# Main execution
try:
    # Connect to the database
    db = mysql.connector.connect(**conn_str)
    cursor = db.cursor()

    # Example transaction: Relate a USER_ACCOUNT to a ROLE
    id_no = 11  # Replace with the user ID you want to update
    role_name = "Manager"  # Replace with the role you want to assign

    # Relate the user to the role
    relate_user_to_role(cursor, id_no, role_name)

    # Fetch and print the updated user account information
    print_user_account(cursor, id_no)

    # Commit the transaction
    db.commit()
    print("Transaction completed successfully!")

except mysql.connector.Error as error:
    print(f"Database error: {error}")
except ValueError as validation_error:
    print(f"Validation error: {validation_error}")
except Exception as generic_error:
    print(f"An error occurred: {generic_error}")
finally:
    # Close resources
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals():
        db.close()



# # 6 Function to Relate an ACCOUNT_PRIVILEGE to a ROLE   #select * from account_privilege_granted to check the update
def assign_account_privilege_to_role(cursor, privilege_name, role_name):
    """Relate an ACCOUNT_PRIVILEGE to a ROLE with validations."""
    print(f"Assigning privilege '{privilege_name}' to role '{role_name}'...")

    # Validate if the privilege exists in ACCOUNT_PRIVILEGE
    validate_privilege_sql = """
    SELECT Privilege_Name
    FROM ACCOUNT_PRIVILEGE
    WHERE Privilege_Name = %s
    """
    cursor.execute(validate_privilege_sql, (privilege_name,))
    privilege = cursor.fetchone()
    if not privilege:
        raise ValueError(f"Privilege '{privilege_name}' does not exist in ACCOUNT_PRIVILEGE. Please add the privilege first.")
    
    print(f"Privilege '{privilege_name}' exists in ACCOUNT_PRIVILEGE.")

    # Validate if the role exists in USER_ROLE
    validate_role_sql = """
    SELECT Role_Name
    FROM USER_ROLE
    WHERE Role_Name = %s
    """
    cursor.execute(validate_role_sql, (role_name,))
    role = cursor.fetchone()
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist in USER_ROLE. Please add the role first.")
    
    print(f"Role '{role_name}' exists in USER_ROLE.")

    # Insert the privilege-role relationship into ACCOUNT_PRIVILEGE_GRANTED
    insert_sql = """
    INSERT INTO ACCOUNT_PRIVILEGE_GRANTED (Privilege_Name, Role_Name)
    VALUES (%s, %s)
    """
    cursor.execute(insert_sql, (privilege_name, role_name))
    print(f"Rows affected: {cursor.rowcount}")

    # Check if the insertion was successful
    if cursor.rowcount == 0:
        raise ValueError(f"Failed to assign privilege '{privilege_name}' to role '{role_name}'.")
    print(f"Privilege '{privilege_name}' successfully assigned to role '{role_name}'.")

def print_account_privileges_for_role(cursor, role_name):
    """Retrieve and print all account privileges assigned to a specific role."""
    sql = """
    SELECT Privilege_Name
    FROM ACCOUNT_PRIVILEGE_GRANTED
    WHERE Role_Name = %s
    """
    cursor.execute(sql, (role_name,))
    results = cursor.fetchall()
    if results:
        print(f"Account Privileges for Role '{role_name}':")
        for privilege in results:
            print(f"- {privilege[0]}")
    else:
        print(f"No privileges found for role '{role_name}'.")

# Main execution
try:
    # Connect to the database
    db = mysql.connector.connect(**conn_str)
    cursor = db.cursor()

    # Example transaction: Relate an ACCOUNT_PRIVILEGE to a ROLE
    privilege_name = "EXECUTE"  # Replace with the privilege you want to assign
    role_name = "tester"  # Replace with the role you want to assign the privilege to

    # Assign the privilege to the role
    assign_account_privilege_to_role(cursor, privilege_name, role_name)

    # Fetch and print all account privileges for the role
    print_account_privileges_for_role(cursor, role_name)

    # Commit the transaction
    db.commit()
    print("Transaction completed successfully!")

except mysql.connector.Error as error:
    print(f"Database error: {error}")
except ValueError as validation_error:
    print(f"Validation error: {validation_error}")
except Exception as generic_error:
    print(f"An error occurred: {generic_error}")
finally:
    # Close resources
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals():
        db.close()



# # 7 Function to Relate a RELATION_PRIVILEGE, ROLE, and TABLE    #select * from ASSIGNED_TABLE_PRIVILEGE

def assign_relation_privilege(cursor, table_name, role_name, privilege_name):
    """Relate a RELATION_PRIVILEGE to a ROLE and TABLE with validations."""
    print(f"Assigning privilege '{privilege_name}' for table '{table_name}' to role '{role_name}'...")

    # Validate if the privilege exists in RELATIONAL_PRIVILEGE
    validate_privilege_sql = """
    SELECT Privilege_Name
    FROM RELATIONAL_PRIVILEGE
    WHERE Privilege_Name = %s
    """
    cursor.execute(validate_privilege_sql, (privilege_name,))
    privilege = cursor.fetchone()
    if not privilege:
        raise ValueError(f"Privilege '{privilege_name}' does not exist in RELATIONAL_PRIVILEGE. Please add the privilege first.")
    
    print(f"Privilege '{privilege_name}' exists in RELATIONAL_PRIVILEGE.")

    # Validate if the role exists in USER_ROLE
    validate_role_sql = """
    SELECT Role_Name
    FROM USER_ROLE
    WHERE Role_Name = %s
    """
    cursor.execute(validate_role_sql, (role_name,))
    role = cursor.fetchone()
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist in USER_ROLE. Please add the role first.")
    
    print(f"Role '{role_name}' exists in USER_ROLE.")

    # Validate if the table exists in TABLE
    validate_table_sql = """
    SELECT Table_Name
    FROM `TABLE`
    WHERE Table_Name = %s
    """
    cursor.execute(validate_table_sql, (table_name,))
    table = cursor.fetchone()
    if not table:
        raise ValueError(f"Table '{table_name}' does not exist in `TABLE`. Please add the table first.")
    
    print(f"Table '{table_name}' exists in `TABLE`.")

    # Insert the relationship into ASSIGNED_TABLE_PRIVILEGE
    insert_sql = """
    INSERT INTO ASSIGNED_TABLE_PRIVILEGE (Table_Name, Role_Name, Privilege_Name)
    VALUES (%s, %s, %s)
    """
    cursor.execute(insert_sql, (table_name, role_name, privilege_name))
    print(f"Rows affected: {cursor.rowcount}")

    # Check if the insertion was successful
    if cursor.rowcount == 0:
        raise ValueError(f"Failed to assign privilege '{privilege_name}' for table '{table_name}' to role '{role_name}'.")
    print(f"Privilege '{privilege_name}' for table '{table_name}' successfully assigned to role '{role_name}'.")

def print_relation_privileges_for_role_and_table(cursor, role_name, table_name):
    """Retrieve and print all relation privileges for a specific role and table."""
    sql = """
    SELECT Privilege_Name
    FROM ASSIGNED_TABLE_PRIVILEGE
    WHERE Role_Name = %s AND Table_Name = %s
    """
    cursor.execute(sql, (role_name, table_name))
    results = cursor.fetchall()
    if results:
        print(f"Relation Privileges for Role '{role_name}' on Table '{table_name}':")
        for privilege in results:
            print(f"- {privilege[0]}")
    else:
        print(f"No privileges found for role '{role_name}' on table '{table_name}'.")

# Main execution
try:
    # Connect to the database
    db = mysql.connector.connect(**conn_str)
    cursor = db.cursor()

    # Example transaction: Relate a RELATION_PRIVILEGE, ROLE, and TABLE
    table_name = "Sales"  # Replace with the table you want to assign the privilege to
    role_name = "Manager"  # Replace with the role
    privilege_name = "SELECT"  # Replace with the privilege name

    # Assign the relation privilege
    assign_relation_privilege(cursor, table_name, role_name, privilege_name)

    # Fetch and print all relation privileges for the role and table
    print_relation_privileges_for_role_and_table(cursor, role_name, table_name)

    # Commit the transaction
    db.commit()
    print("Transaction completed successfully!")

except mysql.connector.Error as error:
    print(f"Database error: {error}")
except ValueError as validation_error:
    print(f"Validation error: {validation_error}")
except Exception as generic_error:
    print(f"An error occurred: {generic_error}")
finally:
    # Close resources
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals():
        db.close()



# # 3.8 Queries to Retrieve Privileges 

# # 3.8.1 Retrieve All Privileges Associated with a ROLE
def get_privileges_for_role(cursor, role_name):
    """
    Retrieve all privileges for a specific role.
    :param cursor: MySQL database cursor
    :param role_name: Role name to retrieve privileges for
    :return: List of privileges
    """
    sql = """
    SELECT DISTINCT Privilege
    FROM (
        SELECT 
            APG.Privilege_Name AS Privilege
        FROM 
            ACCOUNT_PRIVILEGE_GRANTED APG
        WHERE 
            APG.Role_Name = %s

        UNION

        SELECT 
            ATP.Privilege_Name AS Privilege
        FROM 
            ASSIGNED_TABLE_PRIVILEGE ATP
        WHERE 
            ATP.Role_Name = %s
    ) Privileges;
    """
    cursor.execute(sql, (role_name, role_name))
    results = cursor.fetchall()
    return [row[0] for row in results]  # Extract privilege names from the results


#3.8.2 Retrieve All Privileges Associated with a USER_ACCOUNT
def get_privileges_for_user(cursor, id_no):
    """
    Retrieve all privileges for a specific user account.
    :param cursor: MySQL database cursor
    :param id_no: User ID
    :return: List of privileges
    """
    sql = """
    SELECT DISTINCT Privilege
    FROM (
        SELECT 
            APG.Privilege_Name AS Privilege
        FROM 
            USER_ACCOUNT UA
        JOIN 
            ACCOUNT_PRIVILEGE_GRANTED APG
        ON 
            UA.Role_Name = APG.Role_Name
        WHERE 
            UA.Id_No = %s

        UNION

        SELECT 
            ATP.Privilege_Name AS Privilege
        FROM 
            USER_ACCOUNT UA
        JOIN 
            ASSIGNED_TABLE_PRIVILEGE ATP
        ON 
            UA.Role_Name = ATP.Role_Name
        WHERE 
            UA.Id_No = %s
    ) Privileges;
    """
    cursor.execute(sql, (id_no, id_no))
    results = cursor.fetchall()
    return [row[0] for row in results]  # Extract privilege names from the results


#3.8.3 Check Whether a Privilege is Available for a USER_ACCOUNT

def check_privilege_for_user(cursor, id_no, privilege_name):
    """
    Check if a specific privilege is available for a user.
    :param cursor: MySQL database cursor
    :param id_no: User ID
    :param privilege_name: Privilege to check
    :return: True if privilege exists, False otherwise
    """
    sql = """
    SELECT 1
    FROM (
        SELECT 
            APG.Privilege_Name AS Privilege
        FROM 
            USER_ACCOUNT UA
        JOIN 
            ACCOUNT_PRIVILEGE_GRANTED APG
        ON 
            UA.Role_Name = APG.Role_Name
        WHERE 
            UA.Id_No = %s

        UNION

        SELECT 
            ATP.Privilege_Name AS Privilege
        FROM 
            USER_ACCOUNT UA
        JOIN 
            ASSIGNED_TABLE_PRIVILEGE ATP
        ON 
            UA.Role_Name = ATP.Role_Name
        WHERE 
            UA.Id_No = %s
    ) Privileges
    WHERE Privileges.Privilege = %s;
    """
    cursor.execute(sql, (id_no, id_no, privilege_name))
    result = cursor.fetchone()
    return result is not None

try:
    # Connect to the database
    db = mysql.connector.connect(**conn_str)
    cursor = db.cursor()

    # # Task 3.8.1: Retrieve privileges for a ROLE
    role_name = "Manager"  # Replace with the role name to check
    privileges = get_privileges_for_role(cursor, role_name)

    if privileges:
        print(f"Privileges for Role '{role_name}': {', '.join(privileges)}")
    else:
        print(f"No privileges found for Role '{role_name}'.")

    # Task 3.8.2: Retrieve privileges for a USER_ACCOUNT
    user_id = 11  # Replace with the user ID to check
    user_privileges = get_privileges_for_user(cursor, user_id)

    if user_privileges:
        print(f"Privileges for User ID {user_id}: {', '.join(user_privileges)}")
    else:
        print(f"No privileges found for User ID {user_id}.")


    # Task 3.8.3: Check if a privilege is available for a USER_ACCOUNT  #Example: Check if user ID 11 has SELECT privilege 
    user_id = 11
    privilege_to_check = "SELECT"
    has_privilege = check_privilege_for_user(cursor, user_id, privilege_to_check)
    
    if has_privilege:
        print(f"User ID {user_id} has the privilege '{privilege_to_check}'.")
    else:
        print(f"User ID {user_id} does NOT have the privilege '{privilege_to_check}'.")

except mysql.connector.Error as error:
    print("Error during transactions:", error)

finally:
    # Close resources
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals():
        db.close()





    