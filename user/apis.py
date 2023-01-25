from rest_framework import views, response, exceptions, permissions
from .serializers import UserSerializer
from . import services, authentication


class RegisterApi(views.APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        data = serializer.validated_data
        

        serializer.instance = services.create_user(user_dc=data)

    

        return response.Response(data=serializer.data)


class LoginApi(views.APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = services.get_user_by_email(email=email)
        
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        token = services.create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserAPI(views.APIView):
    authentication_classes=(authentication.CustomUserAuth,)
    permission_classes=(permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer= UserSerializer(user)

        return response.Response(serializer.data)


class LogoutAPI(views.APIView):
    authentication_classes=(authentication.CustomUserAuth,)
    permission_classes=(permissions.IsAuthenticated,)

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message":"Logged out"}

        return resp
        
