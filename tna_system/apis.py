## za events dodati crud metode sa autorizacijom 
## za record ne treba autorizacija , ide samo post/put , ako je post onda se unosi in time , ako je put out time 
## dodatna klasa za get records sa autorizacijom 
from rest_framework import views , response, permissions, status
#from .serializers 
import datetime
from django.utils import timezone
from user import  authentication 
from user import  models as usermodels, serializers as userserializer
from . import serializers, services
from . import models



class RecordController(views.APIView):
    authentication_classes=(authentication.CustomUserAuth, )

    def post(self, request, user_id=None):
        try:
            card_id=request.data["card_id"]
            event= request.data["event"]
        except:
            card_id=None
            event=None


        if event != None and models.Event.objects.filter(id=event,is_deleted=False).exists():
            event= models.Event.objects.filter(id=event, is_deleted=False).first()
            if event.start > timezone.now() or event.end < timezone.now():
                return response.Response({"message:Bad request"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return response.Response({"message:Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        if card_id != None and usermodels.User.objects.filter(card_id=card_id, is_deleted=False).exists():
            user = usermodels.User.objects.filter(card_id=card_id, is_deleted=False).first()
        else:
           return response.Response({"message:Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        #ako postoje user i event onda provjeravimo postoji li već zapis za tog studenta , ako postoji onda upisujemo izlazak
        if models.Record.objects.filter(event=event, user=user).exists():
            services.create_record_out(user = user , event = event)
            return response.Response({"message":"Exit record created"}, status=status.HTTP_201_CREATED)
        else:
            
            services.create_record_in(user=user, event = event)
            return response.Response({"message":"Entrance record created"}, status=status.HTTP_201_CREATED)
    
    def get(self,request, user_id=None):
        #get request za records po osobi - +filter po kategoriji 
        # dodati kategorije i postotke za filter
        category= request.GET.get("category", None)

        if not user_id or not  usermodels.User.objects.filter(id=user_id).exists():
            return response.Response({"message:Bad request, user id not provided"}, status=status.HTTP_400_BAD_REQUEST)
        if (request.user.is_staff or request.user.is_superuser) == False:
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        if category:
            if request.user.is_superuser:
                if models.EventCategory.objects.filter(id=category).exists():

                    record_list = models.Record.objects.filter(event__event_category__id=category, user_id = user_id).all()
                else:
                    return response.Response({"message":"Bad request - category doesnt exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if models.EventCategory.objects.filter(event__create_by= request.user, id=category).exists():

                    record_list = models.Record.objects.filter(event__category__id=category, user_id = user_id, event__created_by=request.user).all()
                else:
                    return response.Response({"message":"Bad request - category doesnt exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.user.is_superuser:
                record_list = models.Record.objects.filter( user_id = user_id).all()
            else :
                record_list = models.Record.objects.filter( user_id = user_id, event__created_by=request.user).all()


        
        serializer = serializers.RecordSerializer(record_list, many=True)
        # resp={
        #     "data":serializer.data,
        #     "filters":filter_categories
        # }

       
                

        return response.Response(serializer.data, status=status.HTTP_200_OK)

class UserRecords(views.APIView):
    authentication_classes=(authentication.CustomUserAuth,)

    def get(self,request, user_id=None):
        #get request za records po osobi - +filter po kategoriji 
        # dodati kategorije i postotke za filter
        filter_categories=services.get_categories_and_percentage(request.user, user_id)
        user = usermodels.User.objects.get(id=user_id)
        print(user)
        serializer = userserializer.UserBasicSerializer(user)
        resp={
            "filters":filter_categories,
            "user":serializer.data
        }


        if not user_id or not  usermodels.User.objects.filter(id=user_id).exists():
            return response.Response({"message:Bad request, user id not provided"}, status=status.HTTP_400_BAD_REQUEST)
        if (request.user.is_staff or request.user.is_superuser) == False:
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        


        
        
                

        return response.Response(resp, status=status.HTTP_200_OK)



class EventController(views.APIView):   # /api/event
    authentication_classes=(authentication.CustomUserAuth,)
    permission_classes=(permissions.IsAuthenticated,)



    def post(self, request):
        if not request.user.is_staff :
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.EventPostSerializer(data=request.data)


        if not (models.Location.objects.filter(id=request.data["location"]).exists() or models.EventCategory.objects.filter(id=request.data["event_category"], is_deleted=False).exists()):
            return response.Response({"message":"Bad request "}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        if (data.end<= timezone.now()) or (data.end < data.start) :
            return response.Response({"message":"Bad request : Can't create events in the past"}, status=status.HTTP_400_BAD_REQUEST)
        if services.check_if_availible(data)==False:
            return response.Response({"message:Location is already reserved for that time"}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer.instance = services.create_event(user=request.user, event=data)
        return response.Response({"message:Created"}, status=status.HTTP_201_CREATED)

    #GET doesn't need aditional data , just authenticated user 

    def get(self, request):

        if not request.user.is_staff :
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        category=None
        location=None
        if "category" in request.GET and models.EventCategory.objects.filter(id=int(request.GET.get("category")), is_deleted=False).exists():
            
            category=models.EventCategory.objects.filter(id=int(request.GET.get("category")), is_deleted=False).first()
        if "location" in request.GET and models.Location.objects.filter(id=int(request.GET.get("location")), is_deleted=False).exists(): 
            location = models.Location.objects.filter(id=int(request.GET.get("location")), is_deleted=False).first()

        if "active" in request.GET and request.GET.get("active")=="true":
            active=True
        else:
            active = False
        
        
        #ako je profesor(is_staff), a nije superadmin vraća mu popis predavanja koje je on kreirao
        if (request.user.is_staff) and (not request.user.is_superuser) :
            if (location != None) and (category != None):
                if active:
                    event_list = models.Event.objects.filter(created_by=request.user, location=location, event_category=category, is_deleted=False, end__gte=timezone.now()).all()
                else:
                    event_list = models.Event.objects.filter(created_by=request.user, location=location, event_category=category, is_deleted=False, end__lt=timezone.now()).all()

            if location !=None and category==None:
                if active:
                    event_list = models.Event.objects.filter(created_by=request.user, location=location, is_deleted=False, end__gte=timezone.now()).all()
                else:
                    event_list = models.Event.objects.filter(created_by=request.user, location=location, is_deleted=False, end__lt=timezone.now()).all()
                
            if category != None and location==None:
                if active:
                    event_list = models.Event.objects.filter(created_by=request.user, event_category=category, is_deleted=False, end__gte=timezone.now()).all()
                else:
                    event_list=models.Event.objects.filter(created_by=request.user, event_category=category, is_deleted=False, end__lt=timezone.now()).all()
            if category == None and location==None:
                if active:
                    event_list = models.Event.objects.filter(created_by=request.user, is_deleted=False, end__gte=timezone.now()).all()
                else:
                    event_list = models.Event.objects.filter(created_by=request.user, is_deleted=False, end__lt=timezone.now()).all()


           
            
            serializer = serializers.EventListSerializer(event_list, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        if request.user.is_superuser:
            if location != None and category != None:
                if active:
                    event_list = models.Event.objects.filter( location=location, event_category=category, is_deleted=False, end__gte=timezone.now()).all()
                else:
                    event_list = models.Event.objects.filter( location=location, event_category=category, is_deleted=False, end__lt=timezone.now()).all()

            if location !=None and category==None:
                if active:
                    event_list = models.Event.objects.filter( location=location, is_deleted=False, end__gte=timezone.now()).all()
                else:
                    event_list = models.Event.objects.filter(location=location, is_deleted=False, end__lt=timezone.now()).all()
                
            if category != None and location==None:
                if active:
                    event_list = models.Event.objects.filter(event_category=category, is_deleted=False, end__gte=timezone.now()).all()
                else:
                    event_list=models.Event.objects.filter( event_category=category, is_deleted=False, end__lt=timezone.now()).all()
            if category == None and location==None:
                if active:
                    event_list = models.Event.objects.filter( is_deleted=False, end__gte=timezone.now()).all()
                else:
                    event_list = models.Event.objects.filter( is_deleted=False, end__lt=timezone.now()).all()
            serializer = serializers.EventListSerializer(event_list, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

class EventDetails(views.APIView):
    authentication_classes=(authentication.CustomUserAuth,)

    def get(self, request, event_id):
        if not models.Event.objects.filter(id=event_id).exists():
            return response.Response({"message":"Bad request"})
        
        if not request.user.is_staff :
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        event = models.Event.objects.filter(id=event_id, is_deleted=False).first()
        records = models.Record.objects.filter(event=event).all()
        event_serializer= serializers.EventSerializer(event)
        record_serializer= serializers.RecordBasicSerializer(records, many=True)

        return response.Response({"event":event_serializer.data , "records":record_serializer.data}, status=status.HTTP_200_OK)


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
    


    

        
class SingleEventCategoryController(views.APIView):

    authentication_classes=(authentication.CustomUserAuth,)
    def put(self, request, category=None):
        print(category)
        if not request.user.is_staff :
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if category == None or not models.EventCategory.objects.filter(id=category, is_deleted=False).exists():
            return response.Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializers.EventCategoryUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=serializer.validated_data



        category = models.EventCategory.objects.filter(id=category, is_deleted=False).first()
        category.description = data.description
        category.updated_at = timezone.now()
        category.save()

        return response.Response({"message":"Created"}, status=status.HTTP_201_CREATED)

    def delete(self, request, category=None):
        if not request.user.is_staff :
            return response.Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if category == None or not models.EventCategory.objects.filter(id=category, is_deleted=False).exists():
            return response.Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        
        category = models.EventCategory.objects.filter(id=category, is_deleted=False).first()
        category.is_deleted=True
        category.updated_at = timezone.now()
        category.save()

        return response.Response({"message":"Created"}, status=status.HTTP_201_CREATED)

class NextEvent(views.APIView):
    authentication_classes=(authentication.CustomUserAuth,)
    def get(self, request, location_id=None):

        if location_id==None or not models.Location.objects.filter(id=location_id).exists():
            return response.Response({"message":"Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        delta =timezone.now() + datetime.timedelta(minutes=15)
        if models.Event.objects.filter(is_deleted=False, location__id=location_id, start__lte=delta, end__gte=timezone.now()).exists():


            next = models.Event.objects.filter(is_deleted=False, location__id=location_id, start__lte=delta, end__gte=timezone.now()).first()
            next = serializers.EventSerializer(next)
            next = next.data
            return response.Response(next, status=status.HTTP_200_OK)
        else: 
            return response.Response(status=status.HTTP_204_NO_CONTENT)