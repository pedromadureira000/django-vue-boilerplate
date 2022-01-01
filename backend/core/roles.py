from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions = {
        "create_user": True,
        "delete_users": True,
        "get_all_users": True
    } 

class Reports(AbstractUserRole):
    available_permissions = {
        "check_reports": True
    }
