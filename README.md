# DBMS_AccessControlManagement
# Assumption
1. The database keeps track of USER_ACCOUNTs. Each USER_ACCOUNT has a unique IdNo, a Name, and a Phone no . 
2. The database keeps track of PRIVILEGEs (SELECT, INSERT, DELETE, UPDATE,etc.).  There are two types of privileges: ACCOUNT_PRIVILEGEs and RELATION_PRIVILEGEs: each privilege belongs to only one of the two types. 
3. In addition to USER_ACCOUNTS, the system will keep track of USER_ROLEs. The roles are different for each database application, and new roles can be added at any time. Each USER_ROLE has a unique RoleName, plus possibly other attributes, such as Description. 
4. The database keeps track of TABLEs. Each table has a unique TableName, and is related to a single USER_ACCOUNT who is the owner of the TABLE. 
5. The database will keep track of the current (active) relationships as follows: 
6. The binary relationship between USER_ACCOUNTs and USER_ROLEs (assume that each USER_ACCOUNT is related to exactly one role). 
7. The binary relationship between USER_ROLEs and ACCOUNT_PRIVILEGES. 
8. The ternary relationship between USER_ROLEs, RELATION_PRIVILEGEs, and TABLEs. 
It is assumed that if a role is related to a particular privilege, then all user accounts related to that role will have that privilege 
 
Steps:
1. Extended-Entity Relationship (EER) Schema Diagram was created
2. Mapped the EER schema design to a relational database schema 
3. Created the tables corresponding to the relational schema using the ORACLE DBMS.
4. Specified Constraints in the relational schema.
5. Loaded some data into the database, and applied certain update transactions and retrieval queries.
6. Wrote the following database update transactions using  Python: 

  The first transaction is to add all the information about a new USER_ACCOUNT. 
  
  The second transaction is to add all the information about a new ROLE. 
  
  The third transaction is to add all the information about a new TABLE. This should include specifying the owner user account of the table. 
  
  The fourth transaction is to insert a new PRIVILEGE, including the privilege type. 
  
  The fifth transaction is to relate a USER_ACCOUNT to a ROLE.
  
  The sixth transaction is to relate an ACCOUNT_PRIVILEGE to a ROLE. 
  
  The seventh transaction is to relate a RELATION_PRIVILEGE, ROLE, and TABLE. 
  
  Wrote queries to retrieve all privileges associate with a particular ROLE, and all privileges associated with a particular USER_ACCOUNT. Also, write queries that check whether a particular privilege is currently available (granted) to a particular user account. 

7. Created user friendly Web-based interface for each transaction to enter the information needed by the transaction. 
 
