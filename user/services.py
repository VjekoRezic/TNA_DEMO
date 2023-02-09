import dataclasses
from rest_framework.exceptions import ValidationError
from typing import TYPE_CHECKING
from .models import User
import datetime
import jwt
from django.conf import settings

if TYPE_CHECKING:
    from .models import User

@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    password: str = None
    card_id:str = None
    id: int = None, 
    is_staff: bool =False,
    is_superuser:bool=False,
    is_deleted:bool=False

    @classmethod
    def from_instance(cls, user_dc:"User")->"UserDataClass":
        return cls(
            first_name = user_dc.first_name,
            last_name = user_dc.last_name,
            email = user_dc.email,
            id = user_dc.id,
            card_id = user_dc.card_id, 
            is_staff = user_dc.is_staff,
            is_superuser = user_dc.is_superuser,
            is_deleted = user_dc.is_deleted

        )

def create_user(user_dc: "UserDataClass")->"UserDataClass":
    try: 
        if (User.objects.filter(email=user_dc.email).exists()):
            raise ValidationError(code=400, detail="User with this email already exists")

        instance = User(
            first_name=user_dc.first_name,
            last_name=user_dc.last_name,
            email=user_dc.email,
            card_id=user_dc.card_id,
            is_staff=user_dc.is_staff,
            is_superuser = user_dc.is_superuser, 
            is_deleted = user_dc.is_deleted


        )
        if user_dc.password is not None:
            instance.set_password(user_dc.password)

        instance.save()
        return UserDataClass.from_instance(instance)


    except Exception as e:
        raise ValidationError({"400":f'{str(e)}'})

def get_user_by_email(email:str)-> "User":
        user = User.objects.filter(email=email).first()
        return user
   


def create_token(user_id:int)-> str:
    payload = dict(
        id=user_id,
        exp= datetime.datetime.utcnow() + datetime.timedelta(hours=3) ,
        iat= datetime.datetime.utcnow()
    )
    
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token

