# # # import csv
# # # import json
# # # import os
# # #
# # # from Encryption import Encryption
# # #
# # #
# # #
# # # class User:
# # #
# # #     # def __init__(self,user_name,password):
# # #     #     self.user_name = user_name
# # #     #     self.password = Encryption.encrypt_password(password)
# # #
# # #     def check_password(self,input_pswd):
# # #         """
# # #         Password validation
# # #         :param input_pswd: user password input
# # #         :return: True if the password matches, False otherwise
# # #         """
# # #         return self.password == Encryption.encrypt_password(input_pswd)
# # #
# # #     # def register_user(self,user_name,password):
# # #     #     self.user_name = user_name
# # #     #     self.password = Encryption.encrypt_password(password)
# # #
# # #     def login_user(self,user_name,password):
# # #         """
# # #         Login user
# # #         :param user_name: user input for user name
# # #         :param password: user input for password
# # #         :return: True if login is successful, False otherwise
# # #         """
# # #         return self.check_password(password) and self.user_name == user_name
# # #
# # #     def search_in_csv(self,username,password):
# # #         with open('users.csv','r') as file:
# # #             reader = csv.reader(file)
# # #             rows = list(reader)
# # #             for row in rows:
# # #                 if row[0] == username and row[1] == password:
# # #                     return True
# # #             return False
# # #
# # #     def to_csv_row(self):
# # #         #to put it in a raw of csv file
# # #         return [self.user_name, self.password]
# # #
# # #     def export_to_file(self):
# # #         if os.path.exists("users.csv"): # check if the file exists
# # #             # with open("users.csv","r") as file:  # Open in read mode
# # #             #     first_line = file.readline().strip()  # Read the first row
# # #             #     lines = file.readlines()  # Read all lines into a list
# # #
# # #             with open("users.csv", 'a+', newline="") as file:
# # #                 writer = csv.writer(file)
# # #                 if os.stat("users.csv").st_size == 0:  # check if the file is empty
# # #                     writer.writerow(["Username", "Password"])
# # #                 writer.writerow(self.to_csv_row())
# # #         else:
# # #             with open('users.csv','w',newline="") as file:
# # #                     writer = csv.writer(file)
# # #                     writer.writerow(["Username", "Password"])
# # #                     writer.writerow(self.to_csv_row())
# # #
# # #
# # #
# # #
# # #
# # # if __name__ == '__main__':
# # #     d = User("dor",12345)
# # #     b = User("baruh", "baruhlikesgirls")
# # #     n = User("nadav", "iLikeUri")
# # #     b.export_to_file()
# # #     d.export_to_file()
# # #     n.export_to_file()
# # #
# # import csv
# #
# #
# # def update_copies_in_csv( title, author, genre, year):
# #     with open('books_copy.csv', 'r') as file:
# #         reader = csv.reader(file)
# #         rows = list(reader)
# #         for row in rows:
# #             is_update = False
# #             if row[0] == title and row[1] == author and row[4] == genre and row[5] == str(year):
# #                 row[3] = str(int(row[3]) + 1)
# #                 is_update = True
# #                 break
# #         # if (is_update):
# #         #     with open('books_copy.csv', 'a+') as file:
# #         #         writer = csv.writer(file)
# #         #         writer.writerow(row[3])
# #         if is_update:
# #             with open('books_copy.csv', 'w', newline="") as file:
# #                 writer = csv.writer(file)
# #                 writer.writerows(rows)
# #
# # if __name__ == '__main__':
# #     update_copies_in_csv("The Catcher in the Rye",	"J.D. Salinger", "Fiction",1951)
# import tkinter as tk
# from tkinter import messagebox
#
#
# class UserInfoForm:
#     def __init__(self, root, on_submit_callback):
#         self.root = root
#         self.root.title("User Information Form")
#         self.root.geometry("400x300")
#         self.on_submit_callback = on_submit_callback  # Callback function to forward data
#         self.create_widgets()
#
#     def create_widgets(self):
#         # First Name
#         tk.Label(self.root, text="First Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
#         self.first_name_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
#         self.first_name_entry.grid(row=0, column=1, padx=10, pady=10)
#
#         # Surname
#         tk.Label(self.root, text="Surname:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
#         self.surname_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
#         self.surname_entry.grid(row=1, column=1, padx=10, pady=10)
#
#         # Phone No.
#         tk.Label(self.root, text="Phone No.:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
#         self.phone_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
#         self.phone_entry.grid(row=2, column=1, padx=10, pady=10)
#
#         # Email
#         tk.Label(self.root, text="Email:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
#         self.email_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
#         self.email_entry.grid(row=3, column=1, padx=10, pady=10)
#
#         # Submit Button
#         submit_button = tk.Button(self.root, text="Submit", font=("Arial", 12), command=self.submit_info)
#         submit_button.grid(row=4, column=0, columnspan=2, pady=20)
#
#     def submit_info(self):
#         # Get user inputs
#         first_name = self.first_name_entry.get()
#         surname = self.surname_entry.get()
#         phone_no = self.phone_entry.get()
#         email = self.email_entry.get()
#
#         # Validate inputs
#         if not (first_name and surname and phone_no and email):
#             messagebox.showerror("Error", "All fields must be filled out!")
#             return
#
#         # Call the callback with user data
#         user_data = {
#             "first_name": first_name,
#             "surname": surname,
#             "phone_no": phone_no,
#             "email": email
#         }
#         self.on_submit_callback(user_data)
#
#         # Close the window
#         self.root.destroy()
#
#
# # Function to handle submitted data
# def handle_submission(data):
#     print("Received data:", data)
#     # Forward the data to your main framework or process it further
#
#
# # Run the GUI
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = UserInfoForm(root, handle_submission)
#     root.mainloop()


import tkinter as tk
from tkinter import messagebox


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Screen")
        self.root.geometry("800x400")
        self.root.resizable(True, False)

        # Left Frame
        self.left_frame = tk.Frame(root, bg="#f0f0f0", width=250, height=400)
        self.left_frame.pack(side="left", fill="y")
        tk.Label(self.left_frame, text="Welcome", bg="#f0f0f0", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self.left_frame, text="This is a demo login system.\nPlease login or register to continue.",
                 bg="#f0f0f0", font=("Arial", 12), justify="center").pack(pady=10)

        # Right Frame
        self.right_frame = tk.Frame(root, bg="#ffffff", width=550, height=400)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Form elements
        tk.Label(self.right_frame, text="Login", bg="#ffffff", font=("Arial", 24, "bold")).pack(pady=30)

        tk.Label(self.right_frame, text="Username:", bg="#ffffff", font=("Arial", 14)).pack(pady=5)
        self.username_entry = tk.Entry(self.right_frame, font=("Arial", 14), width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.right_frame, text="Password:", bg="#ffffff", font=("Arial", 14)).pack(pady=5)
        self.password_entry = tk.Entry(self.right_frame, font=("Arial", 14), show="*", width=30)
        self.password_entry.pack(pady=5)

        # Buttons
        self.login_button = tk.Button(self.right_frame, text="Login", font=("Arial", 14), command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.right_frame, text="Register", font=("Arial", 14), bg="#FF3399",
                                         command=self.switch_to_register)
        self.register_button.pack(pady=10)

        self.exit_button = tk.Button(self.right_frame, text="Exit", font=("Arial", 14), command=self.root.quit)
        self.exit_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill out all fields!")
        else:
            messagebox.showinfo("Login", f"Attempting to login user: {username}")

    def register(self):
        messagebox.showinfo("Register", "Redirecting to Register Screen...")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
