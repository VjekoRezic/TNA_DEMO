## za events dodati crud metode sa autorizacijom 
## za record ne treba autorizacija , ide samo post/put , ako je post onda se unosi in time , ako je put out time 
## dodatna klasa za get records sa autorizacijom 
from rest_framework import views , response, exceptions, permissions, status
#from .serializers 
from django.utils import timezone
import datetime
from user import  authentication
from . import serializers, services
from . import models



class EventController(views.APIView):   # /api/event
    authentication_classes=(authentication.CustomUserAuth,)
    permission_classes=(permissions.IsAuthenticated,)



    def post(self, request):
        if not request.user.is_staff :
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.EventPostSerializer(data=request.data)


        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        if (data.end<= timezone.now()) or (data.end < data.start) :
            return response.Response({"message":"Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        if not services.check_if_availible(data):
            return response.Response({"message:Location is already reserved for that time"}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer.instance = services.create_event(user=request.user, event=data)
        return response.Response({"message:Created"}, status=status.HTTP_201_CREATED)

    #GET doesn't need aditional data , just authenticated user 

    def get(self, request):

        if not request.user.is_staff :
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        category=None
        location=None
        if "category" in request.GET and models.EventCategory.objects.filter(name=request.GET.get("category"), is_deleted=False).exists():
            category=models.EventCategory.objects.filter(name=request.GET.get("category"), is_deleted=False).first()
        
        if "location" in request.GET and models.Location.objects.filter(name=request.GET.get("location"), is_deleted=False).exists(): 
            location = models.Location.objects.filter(name=request.GET.get("location"), is_deleted=False).first()

        if "active" in request.GET and request.GET.get("active")==True:
            active=True
        else:
            active = False
        
        
        #ako je profesor(is_staff), a nije superadmin vraća mu popis predavanja koje je on kreirao
        if (request.user.is_staff) and (not request.user.is_superuser) :
            if location and category:
                event_list = models.Event.objects.filter(created_by=request.user, location=location, event_category=category, is_deleted=False).all()
            if location and not category: 
                event_list = models.Event.objects.filter(created_by=request.user, location=location, is_deleted=False).all()
            if category and not location:
                event_list = models.Event.objects.filter(created_by=request.user, event_category=category, is_deleted=False).all()
            if not category and not location:
                event_list = models.Event.objects.filter(created_by=request.user, is_deleted=False).all()


            if active:
                event_list.filter(end__gte = timezone.now())
            else:
                event_list.filter(end__lt = timezone.now())
            serializer = serializers.EventListSerializer(event_list, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        if request.user.is_superuser:
            if location and category:
                event_list = models.Event.objects.filter( location=location, event_category=category, is_deleted=False).all()
            if location and not category: 
                event_list = models.Event.objects.filter(location=location, is_deleted=False).all()
            if category and not location:
                event_list = models.Event.objects.filter(event_category=category, is_deleted=False).all()
            if not category and not location:
                event_list = models.Event.objects.filter( is_deleted=False).all()
            serializer = serializers.EventListSerializer(event_list, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)



class LocationController(views.APIView):
    authentication_classes=(authentication.CustomUserAuth,)

    def get(self, request):
        locations= models.Location.objects.filter(is_deleted=False).all()
        serializer = serializers.LocationSerializer(locations , many=True)
        return response.Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_superuser :
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        serializer.instance = services.create_location(location_dc = data)
        return response.Response({"message":"Created"}, status=status.HTTP_201_CREATED)



class EventCategoryController(views.APIView):

    authentication_classes=(authentication.CustomUserAuth,)
    
    def get(self, request):
        if not request.user.is_staff:
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        categories = models.EventCategory.objects.filter(is_deleted=False).all()
        serializer = serializers.EventCategorySerializer(categories, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        if not request.user.is_staff:
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.EventCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=serializer.validated_data
        serializer.instance = services.create_category(request.user, category=data)
        return response.Response({"message":"Created"}, status=status.HTTP_201_CREATED)
        