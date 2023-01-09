from . import models,schemas
from .utils import hash_password


class UserCrud:

    def create_user(db,payload:schemas.CreateUser):
        password=hash_password(payload.password)
        user=models.User(email=payload.email, password=password, first_name=payload.first_name, last_name=payload.last_name )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user