# utils/constants.py

from enum import Enum

class UserPrivileges(Enum):
    BRANCH_VIEW = "branch message view"
    ADD_USER = "add user"
    EDIT_USER = "edit user"
    DELETE_USER = "delete user"
    VIEW_REPORTS = "view reports"
