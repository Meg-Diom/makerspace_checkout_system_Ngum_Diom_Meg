import sqlite3
from datetime import datetime
from models import Member, Equipment, Loan
connection = sqlite3.connect("makerspace.db")
connection.execute("PRAGMA foreign_keys = ON;")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY,
    member_name TEXT NOT NULL,
    email TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id INTEGER PRIMARY KEY,
    equipment_name TEXT NOT NULL,
    status TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY,
    checkout_date TEXT,
    return_date TEXT,
    status TEXT NOT NULL,
    member_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    FOREIGN KEY (member_id)
        REFERENCES members(member_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (equipment_id)
        REFERENCES equipment (equipment_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
""")

connection.commit()

def add_member(member):
    try:
        cursor.execute("""
            INSERT INTO members (member_id, member_name, email)
            VALUES (?, ?, ?)
        """, (member.member_id, member.member_name, member.email))

        connection.commit()
        
        print("Member added successfully!")
    except sqlite3.IntegrityError:
        print("That member ID already exists!")

def get_members():
    member_objects = []
    cursor.execute("""
        SELECT * FROM members
    """)
    members = cursor.fetchall()
    
    for member in members:
        member_id, member_name, email = member
        member_object = Member(member_id, member_name, email)
        member_objects.append(member_object)
    return member_objects

def update_member(member):
    cursor.execute("""
        UPDATE members SET member_name = ?, email = ? WHERE member_id = ?
    """, (member.member_name, member.email, member.member_id))
    connection.commit()
    print("Member details updated successfully!")

def search_member(search_term):
    cursor.execute("""
        SELECT * FROM members
        WHERE member_name LIKE ?
    """, (f"%{search_term}%",))

    members = cursor.fetchall()
    member_list = []

    for member in members:
        member_id, member_name, email = member
        member_object = Member(member_id, member_name, email)
        member_list.append(member_object)

    return member_list

def add_equipment(equipment):
    try:
        cursor.execute("""
            INSERT INTO equipment (equipment_id, equipment_name, status)
            VALUES (?, ?, ?)
        """, (equipment.equipment_id, equipment.equipment_name, equipment.status))
        connection.commit()
        print("Equipment added successfully!")
    except sqlite3.IntegrityError:
        print("That equipment ID already exists!")

def get_equipment():
    equipment_objects = []
    cursor.execute("""
        SELECT * FROM equipment
    """)
    equipment = cursor.fetchall()
    for tool in equipment:
        equipment_id, equipment_name, status = tool
        equipment_object = Equipment(equipment_id, equipment_name, status)
        equipment_objects.append(equipment_object)
    return equipment_objects

def update_equipment(equipment):
    cursor.execute("""
        UPDATE equipment SET equipment_name = ?, status = ? WHERE equipment_id = ?
    """, (equipment.equipment_name, equipment.status, equipment.equipment_id))
    connection.commit()
    print("Equipment details updated successfully!")


def add_loan(loan):
    checkout_date = (loan.checkout_date.isoformat() if loan.checkout_date else None)
    return_date = (loan.return_date.isoformat() if loan.return_date else None)
    cursor.execute("""
        INSERT INTO loans (loan_id, checkout_date, return_date, status, member_id, equipment_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (loan.loan_id, checkout_date, return_date, loan.status, loan.member_id, loan.equipment_id))
    connection.commit()
    print("Loan added successfully!")

def get_loans():
    loan_objects = []

    cursor.execute("""
        SELECT loan_id, checkout_date, return_date, status, member_id, equipment_id
        FROM loans
    """)

    loans = cursor.fetchall()

    for loan in loans:
        loan_id, checkout_date, return_date, status, member_id, equipment_id = loan

        loan_object = Loan(loan_id, member_id, equipment_id)

        loan_object.checkout_date = (datetime.fromisoformat(checkout_date) if checkout_date else None)
        loan_object.return_date = (datetime.fromisoformat(return_date) if return_date else None)
        loan_object.status = status

        loan_objects.append(loan_object)

    return loan_objects

def update_loan(loan):
    checkout_date = (loan.checkout_date.isoformat() if loan.checkout_date else None)
    return_date = (loan.return_date.isoformat() if loan.return_date else None)
    cursor.execute("""
        UPDATE loans
        SET checkout_date = ?, return_date = ?, status = ?, member_id = ?, equipment_id = ?
        WHERE loan_id = ?
    """, (checkout_date, return_date, loan.status, loan.member_id, loan.equipment_id, loan.loan_id)
    )

    connection.commit()

    print("Loan updated successfully!")

def get_next_loan_id():
    cursor.execute("""
        SELECT MAX(loan_id)
        FROM loans
    """)

    result = cursor.fetchone()[0]

    if result is None:
        return 1

    return result + 1

def get_member_by_id(member_id):
    cursor.execute("""
        SELECT * FROM members WHERE member_id = ?
    """, (member_id,))
    member = cursor.fetchone()
    if member:
        member_id, member_name, email = member
        return Member(member_id, member_name, email)
    return None

def get_equipment_by_id(equipment_id):
    cursor.execute("""
        SELECT * FROM equipment WHERE equipment_id = ?
    """, (equipment_id,))
    tool = cursor.fetchone()

    if tool:
        equipment_id, equipment_name, status = tool
        return Equipment(equipment_id, equipment_name, status)
    return None

def get_loan_by_id(loan_id):
    cursor.execute("""
        SELECT * FROM loans WHERE loan_id = ?
    """, (loan_id,))
    loan = cursor.fetchone()
    if loan:
        loan_id, checkout_date, return_date, status, member_id, equipment_id = loan
        loan_object = Loan(loan_id, member_id, equipment_id)
        loan_object.checkout_date = (datetime.fromisoformat(checkout_date) if checkout_date else None)
        loan_object.return_date = (datetime.fromisoformat(return_date) if return_date else None)
        loan_object.status = status
        return loan_object
    return None
    
def search_equipment(search_term):
    cursor.execute("""
        SELECT * FROM equipment WHERE equipment_name LIKE ?
    """, (f"%{search_term}%",))
    equipment = cursor.fetchall()
    equipment_list = []
    for tool in equipment:
        equipment_id, equipment_name, status = tool
        equipment_object = Equipment(equipment_id, equipment_name, status)
        equipment_list.append(equipment_object)
    return equipment_list

def currently_borrowed_equipments():
    cursor.execute("""
        SELECT e.equipment_id, e.equipment_name, e.status FROM loans AS l
        JOIN equipment AS e
        ON l.equipment_id = e.equipment_id
        WHERE l.status = 'Active'
    """)
    equipment = cursor.fetchall()
    equipment_list = []
    for tool in equipment:
        equipment_id, equipment_name, status = tool
        equipment_object = Equipment(equipment_id, equipment_name, status)
        equipment_list.append(equipment_object)
    return equipment_list

def loan_history():
    cursor.execute("""
        SELECT l.loan_id, m.member_name, e.equipment_name, l.checkout_date, l.return_date, l.status 
        FROM loans as l
        JOIN members AS m
            ON l.member_id = m.member_id
        JOIN equipment AS e
            ON l.equipment_id = e.equipment_id
    """)
    loans = cursor.fetchall()
    for loan in loans:
        loan_id, member_name, equipment_name, checkout_date, return_date, status = loan
        print(f"Loan ID: {loan_id}\nMember Name: {member_name}\nEquipment Name: {equipment_name}\nCheckout Date: {checkout_date}\nReturn Date: {return_date}\nStatus: {status}")
        print(40*"_")

def clear_history():
    confirmation = input(
        "Are you sure you want to clear all loan history? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        cursor.execute("""
            DELETE FROM loans
            WHERE status = 'Returned'
        """)
        connection.commit()
        print("Loan history cleared successfully!")

    else:
        print("Loan history was not cleared.")

def search_loan_by_member(member_id):
    cursor.execute("""
        SELECT l.loan_id, l.checkout_date, l.return_date,
               l.status, l.member_id, l.equipment_id
        FROM loans AS l
        WHERE l.member_id = ?
    """, (member_id,))

    loans = cursor.fetchall()
    loan_list = []

    for loan in loans:
        loan_id, checkout_date, return_date, status, member_id, equipment_id = loan

        loan_object = Loan(loan_id, member_id, equipment_id)

        loan_object.checkout_date = (
            datetime.fromisoformat(checkout_date)
            if checkout_date else None
        )

        loan_object.return_date = (
            datetime.fromisoformat(return_date)
            if return_date else None
        )

        loan_object.status = status

        loan_list.append(loan_object)

    return loan_list

