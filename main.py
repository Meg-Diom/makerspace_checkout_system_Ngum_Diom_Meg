import re
from models import *
from database import *


def checkout_equipment():
    while True:
        try:
            print("\n===== Checkout Equipment =====")
            member_id = int(input("Enter member ID: "))
            equipment_id = int(input("Enter equipment ID: "))
            break
        except ValueError:
            print("Please Enter a number!")
            continue

    member = get_member_by_id(member_id)
    equipment = get_equipment_by_id(equipment_id)

    if not member:
        print("Member not found!")
        return

    if not equipment:
        print("Equipment not found!")
        return

    print(f"Member: {member.member_name}")
    print(f"Equipment: {equipment.equipment_name}")
    print(f"Status: {equipment.status}")

    if not equipment.is_available():
        print("Equipment is not available!")
        return
    loan_id = get_next_loan_id()
    loan = Loan(loan_id, member.member_id, equipment.equipment_id)
    loan.loan_equipment(equipment)

    print(f"Loan ID: {loan.loan_id}")
    print(f"Member ID: {loan.member_id}")
    print(f"Equipment ID: {loan.equipment_id}")
    print(f"Status: {loan.status}")
    print(f"Checkout date: {loan.checkout_date}")
    print(f"Return date: {loan.return_date}")

    add_loan(loan)
    update_equipment(equipment)

def return_equipment():
    while True:
        try:
            loan_id = int(input("Enter the loan_id: "))
            break
        except ValueError:
            print("Please enter a number!")

    loan = get_loan_by_id(loan_id)

    if not loan:
        print("Loan does not exist!")
        return
    
    equipment = get_equipment_by_id(loan.equipment_id)
    result = loan.return_equipment(equipment)
    if result:
        update_loan(loan)
        update_equipment(equipment)

def search():
    search_term = input("Enter equipment name to search: ").strip()
    results = search_equipment(search_term)
    if not results:
        print("Equipment not found!")
    else:
        for result in results:
            result.display_info()

def search_member_menu():
    search_term = input("Enter member name to search: ").strip()

    results = search_member(search_term)

    if not results:
        print("Member not found!")
    else:
        for member in results:
            print(f"Member ID: {member.member_id}")
            member.display_info()
            print(40 * "_")

def search_loan_member():
    while True:
        try:
            member_id = int(input("Enter member ID: "))
            break
        except ValueError:
            print("Please enter a number!")

    member = get_member_by_id(member_id)

    if not member:
        print("Member not found!")
        return

    loans = search_loan_by_member(member_id)

    if not loans:
        print("This member has no loan history!")
        return

    print(f"\nLoan history for {member.member_name}:")
    print(40 * "_")

    for loan in loans:
        print(f"Loan ID: {loan.loan_id}")
        print(f"Equipment ID: {loan.equipment_id}")
        print(f"Checkout Date: {loan.checkout_date}")
        print(f"Return Date: {loan.return_date}")
        print(f"Status: {loan.status}")
        print(40 * "_")

def currently_borrowed():
    results = currently_borrowed_equipments()
    if not results:
        print("No equipment borrowed!")
    else:
        for result in results:
            result.display_info()

def register_member():
    while True:
        try:
            member_id = int(input("Enter member ID: "))
            break
        except ValueError:
            print("Please enter a number!")
            continue
    while True:
        member_name = input("Enter member name: ").strip()

        if member_name:
            break

        print("Member name cannot be empty!")

    while True:
        email = input("Enter email: ").strip()

        if validate_email(email):
            break

        print("Please enter a valid email!")

    member = Member(member_id, member_name, email)

    add_member(member)

def list_members():
    members = get_members()
    print("===== MAKERSPACE MEMBERS=====")
    for member in members:
        member.display_info()

def edit_member():

    while True:
        try:
            member_id = int(input("Enter member ID: "))
            break
        except ValueError:
            print("Please enter a number!")

    member = get_member_by_id(member_id)

    if not member:
        print("Member not found!")
        return

    member.display_info()

    while True:
        new_name = input("Enter new name: ").strip()

        if new_name:
            break

        print("Member name cannot be empty!")

    while True:
        new_email = input("Enter new email: ").strip()

        if validate_email(new_email):
            break

        print("Please enter a valid email!")

    member.update_details(new_name, new_email)
    update_member(member)


def register_equipment():
    while True:
        try:
            equipment_id = int(input("Enter the equipment ID: "))
            break
        except ValueError:
            print("Please enter a number!")
            continue
    while True:
        equipment_name = input("Enter equipment name: ").strip()

        if equipment_name:
            break

        print("Equipment name cannot be empty!")

    equipment = Equipment(equipment_id, equipment_name, "Available")

    add_equipment(equipment)

def list_equipment():
    equipment = get_equipment()
    print("===== MAKERSPACE EQUIPMENT =====")
    for tool in equipment:
        tool.display_info()

def validate_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if re.match(pattern, email):
        return True
    return False

def main():
    try:
        while True:
            print(40*"=")
            print("\tMAKERSPACE CHECKOUT SYSTEM")
            print(40*"=")
            print("1. Register member\n2. List members\n3. Update member\n4. Register equipment")
            print("5. List equipment\n6. Checkout equipment\n7. Return equipment\n8. Search equipment")
            print("9. Search member\n10. Search loan by member\n11. Currently borrowed equipments")
            print("12. Loan history\n13. Clear loan history\n14. Exit")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a number!")
                continue
            if choice == 1:
                register_member()
            elif choice == 2:
                list_members()
            elif choice == 3:
                edit_member()
            elif choice == 4:
                register_equipment()
            elif choice == 5:
                list_equipment()
            elif choice == 6:
                checkout_equipment()
            elif choice == 7:
                return_equipment()
            elif choice == 8:
                search()
            elif choice == 9:
                search_member_menu()
            elif choice == 10:
                search_loan_member()
            elif choice == 11:
                currently_borrowed()
            elif choice == 12:
                loan_history()
            elif choice == 13:
                clear_history()
            elif choice == 14:
                print("Thank you for using our services!")
                break
            else:
                print("Invalid input!")

    except KeyboardInterrupt:
        print("\nProgram was force stopped!")

if __name__ == "__main__":
    main()
