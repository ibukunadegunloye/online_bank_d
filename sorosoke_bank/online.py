# import time

# account_owners = []
# class User:
    
#     def __init__(self,first_name,last_name,username):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.username = username
#         self.account_number = self.__get_account_number()
#         self.account_balance = 0



#     def __get_account_number(self):
#         x = int(time.time())
#         return x

#     def credit_account(self,credit):
#         self.account_balance += credit
        

#     def debit_account(self,debit):
#         self.account_balance -= debit
    


# # def __main ():

    
#     # credit()
#     # User.credit_account(credit())


# def welcome():

#     print("Hello, Welcome to Sorosoke bank!")
#     have_an_account = input("If you have an account with us press --[1] \nIf you would like to create an account with us press --[2] \nPress anything else to exit: ")
#     if have_an_account == '1':
#         user_inputed_acct_no = int(input("Please enter your account number: "))
#         for i in account_owners:
#             if i.account_number == user_inputed_acct_no:
#                 print(f"Welcome {i.first_name} {i.last_name}")
#                 account_management(i)
#             else:
#                 print("Sorry, the account number owner doesnt exist")
#                 welcome()

#     elif have_an_account == '2':
#         account_creator()
#         print ("your account has been succesfully created.")
#         for i in account_owners:
#             account_management(i)
        
#     else:
#             return ("Goodbye, Thanks for banking with us! ")


# def account_creator():
#     print("Welcome to the Account creation portal, please provide your neccessary details below")
#     first_name = input("\nWhat is your first name?: \n")
#     last_name = input("\nWhat is your last name?: \n")
#     username = input("\nWhat is your  username?: \n")
#     user = User(first_name,last_name,username)
#     print(user.account_number)
#     account_owners.append(user)
    

# def account_management(user):

#     while True:
#         user_action = input("Press 1 to credit your account \nPress 2 to debit your account\nPress 3 to check your account balance\nPress 4 to check your account number\nPress anything else to close the application: ")
#         if user_action == '1':
#             credit(user)
#         elif user_action == '2':
#             pass
#             #debit()
#         elif user_action == '3':
#             pass
#         elif user_action == '4':
#             pass
#         else:
#             close_application = int(input("Press 1 to close the application \nPress any other thing to go back to the previous menu"))
#             if close_application == 1:
#                 return ("Goodbye, Thanks for banking with us!")
#             else:
#                 account_management()


# def credit(user):

#     credit_amount = input("\nHow much would you like to credit?: \n")
#     if isinstance(credit_amount,int) or isinstance(credit_amount,float):
#         user.credit_account(credit_amount)
#         print(f"\nAccount {user.account_number} has been credited succesfully. \nYour new account balance is {user.account_balance}\n")
#         print (user.account_number)
#     else:
#         print("wrororororororor")
#         value = ("Wrong input! \nPress 1 to try again, Press 2 to go back to the previous menu \nPress anything else to close the application: ")





# #     print(user.account_balance)
# #     print(user.credit_account(200))
# #     print(user.account_balance)
# #     print(user.account_number)



# # __main()

# welcome()

# #use isinstance to check when inputs are floats and or ints

# # # p1 = User("ade","oni","deni")

# # # print(p1.credit_account(200))
# # # print(p1.get_account_balance)
# # # print (int(time.time()) )

def test(a,**ar):
    print(ar)

test(1,2,3,4)