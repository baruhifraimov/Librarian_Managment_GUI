# import csv
# import json
# import os
#
# from Encryption import Encryption
#
#
#
# class User:
#
#     # def __init__(self,user_name,password):
#     #     self.user_name = user_name
#     #     self.password = Encryption.encrypt_password(password)
#
#     def check_password(self,input_pswd):
#         """
#         Password validation
#         :param input_pswd: user password input
#         :return: True if the password matches, False otherwise
#         """
#         return self.password == Encryption.encrypt_password(input_pswd)
#
#     # def register_user(self,user_name,password):
#     #     self.user_name = user_name
#     #     self.password = Encryption.encrypt_password(password)
#
#     def login_user(self,user_name,password):
#         """
#         Login user
#         :param user_name: user input for user name
#         :param password: user input for password
#         :return: True if login is successful, False otherwise
#         """
#         return self.check_password(password) and self.user_name == user_name
#
#     def search_in_csv(self,username,password):
#         with open('users.csv','r') as file:
#             reader = csv.reader(file)
#             rows = list(reader)
#             for row in rows:
#                 if row[0] == username and row[1] == password:
#                     return True
#             return False
#
#     def to_csv_row(self):
#         #to put it in a raw of csv file
#         return [self.user_name, self.password]
#
#     def export_to_file(self):
#         if os.path.exists("users.csv"): # check if the file exists
#             # with open("users.csv","r") as file:  # Open in read mode
#             #     first_line = file.readline().strip()  # Read the first row
#             #     lines = file.readlines()  # Read all lines into a list
#
#             with open("users.csv", 'a+', newline="") as file:
#                 writer = csv.writer(file)
#                 if os.stat("users.csv").st_size == 0:  # check if the file is empty
#                     writer.writerow(["Username", "Password"])
#                 writer.writerow(self.to_csv_row())
#         else:
#             with open('users.csv','w',newline="") as file:
#                     writer = csv.writer(file)
#                     writer.writerow(["Username", "Password"])
#                     writer.writerow(self.to_csv_row())
#
#
#
#
#
# if __name__ == '__main__':
#     d = User("dor",12345)
#     b = User("baruh", "baruhlikesgirls")
#     n = User("nadav", "iLikeUri")
#     b.export_to_file()
#     d.export_to_file()
#     n.export_to_file()
#
