MAKERSPACE CHECKOUT SYSTEM

DESCRPTION AND FEATURES

The Makerspace Checkout system is a python based command line based application that manages members, equipments and equipment loans in a makerspace system. The application uses object oriented programming to represent members,
equipments and loans, and SQL to manage and store data. The system uses a command line interface with a menu provided so the user can interract. The system provides a series of features which include;
Register a new member, List all members, Update member information, Register equipment, List all equipment, Checkout equipment, Return equipment, Search for equipment, View currently borrowed equipment, View loan history,
Validate user input, Handles errors.

TOOLS USED

The tools used to implement this application includes;
Python3, SQLIte3, Object Oriented Programming and Regular Expressions

PROJECT STRUCTURE

. 
├── main.py 
├── models.py
├── database.py
├── makerspace.db
└── README.md

main.py

Contains the main application logic and user interface.

It is responsible for:

Displaying the menu
Getting user input
Validating user input
Calling the appropriate functions
Managing the flow of the application
models.py

Contains the classes used by the application.

The main classes are:

Member
Equipment
Loan

These classes represent the objects used by the system and contain their related behaviors.

database.py

Handles the SQLite database.

It is responsible for:

Creating database tables
Adding records
Retrieving records
Updating records
Deleting records
Searching equipment
Retrieving loan information
makerspace.db

SQLite database containing the application's persistent data.

DATABASE STRUCTURE

The database uses 3 main tables;
Members table stores unformation about registered users such as member_id which uniquely identifies the member, member_name which stores the name of the member and email which stores a user's email. 
Equipment table stores information about the equipment such as equipment_id which uniquely identifies an equipment, equipment_name which stores the name of the equipment and status which shows wether an an equipment iia available or 
it is currently borrowed. 
Loan table stores information about the loan such as the loan_id which is generated automatically and uniquely identifies a loan, checkout_date which is also ngenerated when the loan is created, return_date which stores the date the 
equipment is returned, member_id and equipment_id which stores the member_id of the user borrowing an equipment and the equipment being borrowed. 
 
HOW TO RUN

Make sure Python 3 is installed.

From the project directory, run:

python3 main.py

The application will display the main menu:

============================================================
        MAKERSPACE CHECKOUT SYSTEM
============================================================
1. Register member
2. List members
3. Update member
4. Register equipment
5. List equipment
6. Checkout equipment
7. Return equipment
8. Search equipment
9. Currently borrowed equipments
10. Loan history
11. Exit

Enter the number corresponding to the operation you want to perform.

Example

A typical checkout process is:

Register a member.
Register equipment.
Select Checkout equipment.
Enter the member ID.
Enter the equipment ID.
The system verifies that both exist.
The system verifies that the equipment is available.
A loan is created.
The equipment status changes to Borrowed.

When the equipment is returned:

Select Return equipment.
Enter the loan ID.
The system updates the loan status to Returned.
A return date is recorded.
The equipment status changes back to Available.
