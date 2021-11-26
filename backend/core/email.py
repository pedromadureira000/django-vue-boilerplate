from djoser import email

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "password_reset.html"
