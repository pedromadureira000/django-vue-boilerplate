from rolepermissions.roles import AbstractUserRole

#  ------------------------/User/---------------------

#  ------------------------/Orders/---------------------

#  class GenerateBoleto(AbstractUserRole):
    #  available_permissions = {
        #  'generate_boleto': True
    #  }


#  ------------------------/Documents/---------------------

class GenerateBoleto(AbstractUserRole):
    available_permissions = {
        'generate_boleto': True
    }

