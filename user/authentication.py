from django.conf import settings
from rest_framework import authentication, exceptions
import jwt


from . import models
# Autentikacija za custom user klasu
class CustomUserAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:#ako nema tokena ne vraćamo ništa
            return None
        
        try: #ako ima token dekodiraj pokušaj dekodirat i vratit korisnika
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            

        except: #ako ne uspije dekodiranje podigni autentication error
            raise exceptions.AuthenticationFailed("Unauthorized")
        
        user= models.User.objects.filter(id=payload["id"]).first()

        return(user, None)

        