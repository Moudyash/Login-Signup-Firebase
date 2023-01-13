import sys
import re
import bcrypt as bcrypt
import firebase_admin
from PyQt5 import QtCore, QtGui, QtWidgets
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore as firestore
cred = credentials.Certificate(
    r"C:\Users\Medo\PycharmProjects\pyfirebase\python-26976-firebase-adminsdk-blclh-5f7920e509.json")
class WelcomeScreen(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Welcome")

        # Create a label to display the welcome message
        self.label = QtWidgets.QLabel("Welcome " + username + "!")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # Set the label as the central widget
        self.setCentralWidget(self.label)

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Initialize Firebase
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        # Create widgets for the login form
        self.username_label = QtWidgets.QLabel("Username:")
        self.username_edit = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel("Password:")
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton("Login")
        self.create_account_button = QtWidgets.QPushButton("Create new account")

        self.create_account_button.clicked.connect(self.show_signup_dialog)


        # Set icon to username edit text
        self.username_edit.setTextMargins(5, 0, 0, 0)
        self.username_edit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.username_edit.setStyleSheet("QLineEdit {padding-left: 30px;}")
        self.username_edit.setClearButtonEnabled(True)
        self.username_edit.setPlaceholderText("Enter Your Email")
        self.username_edit.setTextMargins(5, 0, 0, 0)
        self.username_edit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.username_edit.setStyleSheet("QLineEdit {padding-left: 30px;}")


        # Set icon to password edit text
        self.password_edit.setTextMargins(5, 0, 0, 0)
        self.password_edit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.password_edit.setStyleSheet("QLineEdit {padding-left: 30px;}")
        self.password_edit.setClearButtonEnabled(True)
        self.password_edit.setPlaceholderText("Enter Your Password")
        self.password_edit.setTextMargins(5, 0, 0, 0)
        self.password_edit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.password_edit.setStyleSheet("QLineEdit {padding-left: 30px;}")

        # Create a grid layout and add the widgets
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username_edit, 0, 1)
        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password_edit, 1, 1)
        grid_layout.addWidget(self.login_button, 2, 0, 1, 2)
        grid_layout.addWidget(self.create_account_button, 3, 0, 1, 2)
        self.setLayout(grid_layout)

        # Set the window properties
        self.setWindowTitle("Login")
        self.resize(400, 150)

        # Connect the login button to the login function
        self.login_button.clicked.connect(self.login)

    def login(self):

        # Get the inputted data
        email = self.email_edit.text()
        password = self.password_edit.text()

        # Sign in with email and password
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print("Successfully signed in as: {0}".format(user.uid))

        except Exception as e:
            print("Error signing in:", e)
            self.email_edit.setFocus()
            return

    def show_signup_dialog(self):
        # Create a new dialog for the sign-up form
        signup_dialog = SignupDialog(self)
        signup_dialog.exec_()


class SignupDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create widgets for the sign-up form
        self.username_label = QtWidgets.QLabel("Username:")
        self.username_edit = QtWidgets.QLineEdit()
        self.email_label = QtWidgets.QLabel("Email:")
        self.email_edit = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel("Password:")
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup_button = QtWidgets.QPushButton("Sign Up")
        self.signup_button.setStyleSheet("QPushButton {background-color: blue;}")

        # Create a grid layout and add the widgets
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username_edit, 0, 1)
        grid_layout.addWidget(self.email_label, 1, 0)
        grid_layout.addWidget(self.email_edit, 1, 1)
        grid_layout.addWidget(self.password_label, 2, 0)
        grid_layout.addWidget(self.password_edit, 2, 1)
        grid_layout.addWidget(self.signup_button, 3, 0, 1, 2)
        self.setLayout(grid_layout)

        # Set the window properties
        self.setWindowTitle("Sign Up")
        self.resize(400, 150)

        # Connect the signup button to the signup function
        self.signup_button.clicked.connect(self.signup)

    def signup(self):
        # Get the inputted email and password
        email = self.email_edit.text()
        password = self.password_edit.text()
        username = self.username_edit.text()
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QtWidgets.QMessageBox.warning(self, "Signup Failed", "Invalid Email.")
            self.email_edit.setFocus()
            return
        # Create a new user with email and password
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            db = firestore.client().collection("users").document(username).set({
                "username": username,
                "email": email
            })
            print(" new user:", username)
            print("Successfully created new user: {0}".format(user.uid))
        except Exception as e:
            print("Error creating new user:", e)
            self.email_edit.setFocus()
            return

        # save the user's data in firestore


        QtWidgets.QMessageBox.information(self, "Signup Successful", "Your account has been created successfully.")
        self.accept()
        '''
        # Encrypt the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QtWidgets.QMessageBox.warning(self, "Signup Failed", "Invalid Email.")
            self.email_edit.setFocus()
            return

        # Check if the email is not already taken
        doc = self.db.collection("users").where("email", "==", email).get()
        if doc:
            QtWidgets.QMessageBox.warning(self, "Signup Failed", "Email already taken.")
            self.email_edit.setFocus()
        else:
            # Save the new user to the "users" collection
            self.db.collection("users").add({
                "email": email,
                "password": hashed_password.decode()
            })
            QtWidgets.QMessageBox.information(self, "Signup Successful", "Your account has been created successfully.")
            self.accept()
            LoginDialog(QtWidgets.QDialog)
            '''
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login_dialog = LoginDialog()
    login_dialog.show()
    sys.exit(app.exec_())
