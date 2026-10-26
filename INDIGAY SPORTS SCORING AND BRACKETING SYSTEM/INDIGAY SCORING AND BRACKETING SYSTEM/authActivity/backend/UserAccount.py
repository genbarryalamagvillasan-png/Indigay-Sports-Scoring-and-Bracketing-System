import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

SCHOOL_DOMAIN = "@my.smciligan.edu.ph"

COLLEGES = [
    "CON",
    "CHTM",
    "COC",
    "CED",
    "COE",
    "CAS",
    "CCS",
    "SHS",
    "CBAA",
    "JHS",
]


def clean_name(name):
    name = name.lower()
    name = name.replace(" ", "")
    name = name.replace("ñ", "n")
    return name


def make_username(firstname, middlename, lastname):
    first = clean_name(firstname)
    middle = clean_name(middlename)
    last = clean_name(lastname)

    if first == "" or last == "":
        return ""

    return first + middle + "." + last + SCHOOL_DOMAIN


class UserAccount:
    def __init__(self, filename=None):
        if filename is None:
            filename = os.path.join(BASE_DIR, "data", "accounts.txt")
        self.filename = filename
        self.accounts = {}
        self.current_user = None
        self.role = None

        self.create_file()
        self.load_accounts()

    def create_file(self):
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def load_accounts(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")

                if len(parts) < 7:
                    continue

                username = parts[0]
                self.accounts[username] = {
                    "password": parts[1],
                    "role": parts[2],
                    "college": parts[3],
                    "firstname": parts[4],
                    "middlename": parts[5],
                    "lastname": parts[6]
                }

    def save_accounts(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            for username in self.accounts:
                acc = self.accounts[username]
                f.write(username + "," + acc["password"] + "," + acc["role"] + "," +
                        acc["college"] + "," + acc["firstname"] + "," +
                        acc["middlename"] + "," + acc["lastname"] + "\n")

    def register(self, firstname, middlename, lastname, password, confirmpass, college):
        firstname = firstname.strip()
        middlename = middlename.strip()
        lastname = lastname.strip()

        if firstname == "":
            return "Please enter your first name"
        if lastname == "":
            return "Please enter your last name"
        if college not in COLLEGES:
            return "Please select your college"
        if len(password) < 6:
            return "Password should be at least 6 characters"
        if password != confirmpass:
            return "Passwords do not match"

        if "," in firstname + middlename + lastname + password:
            return "Commas are not allowed"

        if "|" in firstname + middlename + lastname:
            return "The | symbol is not allowed in names"

        username = make_username(firstname, middlename, lastname)

        if username in self.accounts:
            return "User already exists"

        self.accounts[username] = {
            "password": password,
            "role": "student",
            "college": college,
            "firstname": firstname,
            "middlename": middlename,
            "lastname": lastname
        }
        self.save_accounts()
        return "Registration successful!"

    def login(self, username, password, role):
        username = username.strip().lower()

        if role == "student" and not username.endswith(SCHOOL_DOMAIN):
            return "Please use your school email (" + SCHOOL_DOMAIN + ")"

        if username not in self.accounts:
            return "User not found!"

        if self.accounts[username]["password"] != password:
            return "Password Incorrect!"

        if self.accounts[username]["role"] != role:
            return "Wrong role!"

        self.current_user = username
        self.role = role

        return "Login successful!"

    def get_firstname(self):
        if self.current_user in self.accounts:
            firstname = self.accounts[self.current_user]["firstname"]
            if firstname != "":
                return firstname
        return self.current_user

    def get_fullname(self, username):
        if username not in self.accounts:
            return username

        acc = self.accounts[username]
        fullname = acc["firstname"]

        if acc["middlename"] != "":
            fullname = fullname + " " + acc["middlename"]

        fullname = fullname + " " + acc["lastname"]
        return fullname

    def password(self, username, newpass, confirmpass):
        username = username.strip().lower()

        if username not in self.accounts or self.accounts[username]["role"] != "student":
            return "User not found"

        if len(newpass) < 6:
            return "Password should be at least 6 characters"

        if "," in newpass:
            return "Commas are not allowed"

        if newpass != confirmpass:
            return "Passwords do not match"

        self.accounts[username]["password"] = newpass
        self.save_accounts()

        return "Password changed successfully!"
