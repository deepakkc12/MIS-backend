# import random
# from typing import List
# # from ..models.Models import Ean,EanPrice,Users as UserModel,userMenuOption,UserBranches
# from ..Core import db
# from ..utils.helpers import get_current_date
# from .Authentication import AuthUser
# from ..utils.exceptions import NotFoundError 

# from ..utils.Encryptor import AESCipher

# class Users(UserModel):

#     encrypter = AESCipher()

#     @classmethod
#     def branch_wise_list(cls,branch_code):

#         query = """SELECT LoginCode,Code,Username,DOT,LicenceCode From Users WITH (NOLOCK) WHERE BranchCode = ?"""

#         param = [branch_code]

#         result = db.get_data(query=query,data=param)

#         return result
    

#     def find_existing_privilege(self,option_code,connection = db):
#         querry = """SELECT Code From userMenuOption WITH (NOLOCK) WHERE userCode=? and menuOptionCode = ?"""

#         param = [self.Code,option_code]

#         result = connection.get_data(query=querry,data=param)

#         return result
    
#     def add_all_privileges(self):
#         master_privileges = Users.get_master_privileges()
#         for master in master_privileges:

#             master_code = master['code']

#             self.add_privilege(menu_option_code=master_code)




#     def add_privilege(self,menu_option_code):

#         user_menu_option = userMenuOption()

#         user_menu_option.userCode = self.Code

#         user_menu_option.menuOptionCode = menu_option_code

#         with db.transaction() as trans:

#             existing_privilege = self.find_existing_privilege(option_code=menu_option_code,connection=trans)

#             if existing_privilege:
#                 return
            
#             else:
#                return user_menu_option.save(connection=trans)
            

        
#     def get_user_privileges(self):
#         query = """SELECT umo.*,mo.name  From userMenuOption umo WITH (NOLOCK) Join MenuOptions mo ON umo.menuOptionCode = mo.code Where userCode = ?"""

#         param = [self.Code]

#         result = db.get_data(query=query,data=param)

#         return result
    
#     @classmethod
#     def get_master_privileges(cls):
#         query = """SELECT * FROM MenuOptions WITH (NOLOCK)"""

#         result = db.get_data(query=query)

#         return result


#     def remove_privilege(self,user_menu_option_code):
#         query = """delete from userMenuOption where code = ?"""
#         param = [user_menu_option_code]

#         print(user_menu_option_code)

#         result = db.delete(query=query,data=param)

#         print(result)

#         if result ==1:
#             return True
#         return False
    
#     @staticmethod
#     def generate_unique_4_digit_number():
#         # Generate a random 4-digit number
#         return random.randint(1000, 9999)
    
#     def generate_pin(self)->int:
        
#         query = """SELECT CODE FROM USERS WITH (NOLOCK) WHERE PIN = ?"""

#         pin = self.generate_unique_4_digit_number()
#         param = [pin]

#         result = db.get_data(query=query,data=param)

#         if not result:
#             self.Pin = pin
#             return pin
        
#         else:
#             self.generate_pin()


    

#     def validate_login_code(self)->bool:

#         query = """SELECT CODE FROM USERS WITH (NOLOCK) WHERE LOGINCODE = ?"""
#         param = [self.LoginCode]

#         result = db.get_data(query=query,data=param)

#         if not result:
#             return True
#         else:
#             return False

    
#     def validate_username(self)->bool:

#         query = """SELECT CODE FROM USERS WITH (NOLOCK) WHERE username = ?"""
#         param = [self.Username]

#         result = db.get_data(query=query,data=param)

#         if not result:
#             return True
#         else:
#             return False
        
#     @classmethod
#     def generate_enc_pin(cls,pin):
       
#        cipher = AESCipher()

#        enc_pin = cipher.encrypt(data=pin)

#     #    cls.encPin = enc_pin
#        return enc_pin


#     def validate(self):
#         username_error = ""
#         login_code_error = ""

#         valid_username = self.validate_username()
#         valid_login_code = self.validate_login_code()

#         print(valid_username,valid_login_code)

#         if not valid_username:
#             username_error = "Username already exists"
#         if not valid_login_code:
#             login_code_error = "Login code already exists"

#         # Construct the error message
#         error_message = username_error
#         if login_code_error:
#             error_message += f" & {login_code_error}" if username_error else login_code_error

#         return error_message.strip()

        
#     def save(self, connection=db):

#         self.IsActive = 1
#         self.StartupUI = 'TPOS2'
        
#         validation_errors = self.validate()

#         if validation_errors:
#             raise ValueError(f"Validation failed: {validation_errors}")

#         self.DOT = get_current_date()
#         self.Username = self.Username
#         self.generate_pin()
#         self.Pswd = self.Pin
        
#         self.BranchCode = self.BranchCode

#         self.LicenceCode = self.BranchCode

#         self.LoginCode = self.LoginCode

#         self.IsAdmin = 0

#         print(f"pindinininicenkcm.././,.{self.Pin}")

#         self.encPin = self.generate_enc_pin(self.Pin)

#         # print(self.encPin,self.Pin)

#         # query = """select encPin from users where logincode = 'Demo1'"""
#         # result = db.get_data(query=query,)

#         # print(result[0]['encPin'])

#         # cipher = AESCipher()

#         # pin = cipher.decrypt('DzUNPOHzjYvVqN32Y/9TsQ==')

#         # raise Exception(f"enc pin is {pin}")
        
#         super().save(connection=connection)

#         return self.to_dict()
    

    

#     @classmethod
#     def change_password(cls,user_code: int, old_password: str, new_password: str) -> bool:
#             """Change user's password."""

#             if not (1000 <= new_password <= 9999):
#                 raise ValueError("Password must be a 4-digit number")

#             cipher = AESCipher()

#             # Hash passwords
#             old_hash = cipher.encrypt(old_password)
#             new_hash = cipher.encrypt(new_password)

#             # enc_pin = cls.generate_enc_pin(pin=new_hash)
            
#             # Verify old password and update to new one

#             query = """
#                 UPDATE Users
#                 SET Pswd = ?,encPin = ?,pin = ?
#                 WHERE Code = ? AND encPin = ?
#             """

#             user = cls()

#             user.Pswd = new_password
#             user.Pin = new_password

#             user.encPin = new_hash

#             # raise Exception(new_hash)

#             updated_row = db.update(query, [user.Pswd,user.encPin,user.Pin, user_code, old_hash])

#             if updated_row ==1:
#                 return True
#             else :
#                 raise ValueError("User not found")
            
#     def update_branch_code(self,branch_code):
#         query ="""update users set branchCode =? where code =?"""

#         params = [branch_code,self.Code]

#         result = db.update(query=query,data=params)

#         if result ==1:
#             return True
#         else:
#             raise Exception("branch Updation failed ")
        
#     def assign_branch(self,branch_code,login_code):

#         user_branch = UserBranches()

#         user_branch.UserCode = self.Code
#         user_branch.BranchCode = branch_code

#         user_branch.LoginCode = login_code

#         user_branch.DOT = get_current_date()

#         user_branch.LoginCode = user_branch.LoginCode

#         user_branch.save()

#         return user_branch

        


#     def get_assigned_branches(self):

#         query = """SELECT UB.*,B.Name As BranchName from UserBranches UB JOIN Branches B ON UB.BranchCode = B.Code  WHERE UB.UserCode = ? """

#         param = [self.Code]

#         user_branhces = db.get_data(query=query,data=param)

#         return user_branhces
    

#     @classmethod
#     def remove_assigned_branch(cls,userBranchCode):
#         query = """delete from UserBranches where Code = ?"""

#         param = [userBranchCode]

#         db.delete(query=query,data=param)

#         return True



        










