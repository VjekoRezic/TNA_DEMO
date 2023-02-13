from rest_framework import views, response, exceptions, permissions, status
from .serializers import UserSerializer
from . import services, authentication , models
from tna_system import models as tna_models



class RegisterApi(views.APIView): # /api/register
#request example
# {
# "first_name":"vjeko",
# "last_name":"rezic",
# "email":"vjekogmf@gmail.com",
# "password":"test",
# "card_id":"0007787585"
# }
    authentication_classes=(authentication.CustomUserAuth,)
    permission_classes=(permissions.IsAuthenticated,)
    def post(self, request):
        if not request.user.is_superuser:
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        print(request.data)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        data = serializer.validated_data
        

        serializer.instance = services.create_user(user_dc=data)

    

        return response.Response(data=serializer.data)


class LoginApi(views.APIView): #/api/login

#request example
# {
# "email":"vjekogmf@gmail.com",
# "password":"test"
# }

    def post(self, request):
        try:
            email = request.data["email"]
            password = request.data["password"]

            user = services.get_user_by_email(email=email)
        except: 
            return response.Response(data={"message":"Bad Request"}, status = status.HTTP_400_BAD_REQUEST)
        
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        token = services.create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True, secure= True , samesite="None")

        return resp

class UserListApi(views.APIView):
    authentication_classes=(authentication.CustomUserAuth,)
    permission_classes=(permissions.IsAuthenticated,)

    def get(self, request):
        if not (request.user.is_superuser or request.user.is_staff):
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser:
            userlist = models.User.objects.filter(is_deleted=False, is_staff=False, is_superuser=False).all()
            


        else :
            userids= tna_models.Record.objects.values_list('user').filter(event__created_by=request.user).distinct()
            userlist=models.User.objects.filter(id__in=userids, is_deleted=False, is_staff=False, is_superuser=False).all()
            
        serializer = UserSerializer(userlist, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
        

class UserAPI(views.APIView): # /api/me
    authentication_classes=(authentication.CustomUserAuth,)
    permission_classes=(permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        

        serializer= UserSerializer(user)

        return response.Response(serializer.data)


class LogoutAPI(views.APIView): # /api/logout
    authentication_classes=(authentication.CustomUserAuth,)
    permission_classes=(permissions.IsAuthenticated,)

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message":"Logged out"}

        return resp
        
