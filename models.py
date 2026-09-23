from datetime import datetime, timedelta

class Member:

    def __init__(self, member_id, member_name, email):
        self.member_id = member_id
        self.member_name = member_name
        self.email = email

    def display_info(self):
        print(f"Name: {self.member_name}\nEmail: {self.email}")

    def update_details(self, new_name, new_email):
        self.member_name = new_name
        self.email = new_email
        print("Member updated successfully!")

class Equipment:

    def __init__(self, equipment_id, equipment_name, status):
        self.equipment_id = equipment_id
        self.equipment_name = equipment_name
        self.status = status

    def is_available(self):
        return self.status == "Available"

    def display_info(self):
        print(f"Equipment: {self.equipment_name}\nStatus: {self.status}")

    def update_status(self, new_status):
        self.status = new_status


class Loan:

    def __init__(self, loan_id, member_id, equipment_id):
        self.loan_id = loan_id
        self.member_id = member_id
        self.equipment_id = equipment_id
        self.checkout_date = None
        self.return_date = None
        self.status = "Pending"

    def loan_equipment(self, equipment):
        if self.status == "Pending":
            if equipment.is_available():
                self.checkout_date = datetime.now()
                self.status = "Active"
                equipment.update_status("Borrowed")

                print("Equipment Borrowed!")
            else:
                print("Equipment is not available!")
        elif self.status == "Active":
            print("This loan is currently active!")
        elif self.status =="Returned":
            print("This loan has already been returned!")

    def return_equipment(self, equipment):
        if self.status == "Active":
            self.return_date = datetime.now()
            self.status = "Returned"

            equipment.update_status("Available")

            print("Equipment is now available!")
            return True
        else:
            print("This loan has already been returned!")
            return False
