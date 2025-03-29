from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, id_number, phone_number, age, full_name, password=None, **extra_fields):
        if not id_number:
            raise ValueError("Users must have an ID number.")
        user = self.model(
            id_number=id_number,
            phone_number=phone_number,
            age=age,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

