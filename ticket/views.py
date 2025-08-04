from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import Event,EventSerializer,RegisterSerializer,LoginSerializer,Booking,BookingSerializer,TicketSerializer,Ticket
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from django.db.models import Q
from rest_framework import status as http_status
# Create your views here.

class PublicEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']

    @action(detail=False,methods=['GET'])
    def search_events(self,request):
        search = request.GET.get('search')
        events = Event.objects.all()
        if search:
            events = events.filter(Q(title__icontains=search)|Q(descritpion__icontains = search))
        searilizer = EventSerializer(events,many=True)
        
        return Response({
            "status":True,
            "message":"Data fetched successfully",
            "data":searilizer.data
        })
        
    # def create(self, request):
    #     raise MethodNotAllowed('POST')
    # def create(self,request):
    #     raise MethodNotAllowed("PUT")
    # def create(self,request):
    #     raise MethodNotAllowed('PATCH')
    # def create(self,request):
    #     raise MethodNotAllowed('DELETE')


class PrivateEventVeiwSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class TicketViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class BookingViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        data = request.data
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            data = serializer.validated_data
            ticket = data.get('ticket')
            user = data.get('user')
            status = data.get('status')
            quantity = data.get('quantity')
            # try:
            #     ticket = Ticket.objects.get(id = ticket_id)
            #     user = User.objects.get(id=user_id)
            # except Ticket.DoesNotExist:
            #     return Response({"status": False, "message": "Invalid ticket ID"}, status=http_status.HTTP_400_BAD_REQUEST)
            # except User.DoesNotExist:
            #     return Response({"status": False, "message": "Invalid user ID"}, status=http_status.HTTP_400_BAD_REQUEST)
            
            total_price = quantity*ticket.price
            if request.user == user:
                Booking.objects.create(ticket=ticket,user=user,status=status,quantity=quantity,total_price=total_price)
                return Response({"status":True,"message":"Booking confirmend"})
        return Response({
            "status":False,
            "message":"Validation Error",
            "erros":serializer.errors
        },status=http_status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        query = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(query,many=True)

        
        return Response({
            "status":True,
            "message":"data fetched",
            "Ticket": serializer.data
        })
    
        # return Response({
        #     "status":False,
        #     "message":"something went wrong",
        #     "errors":serializer.errors
        # })




class RegisterApi(APIView):  
    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":True,
                "message":"User created successfully",
                "data":serializer.data
            },status=201)
        return Response({
            "status":False,
            "message":"Something went wrong",
            "errors":serializer.errors
        })
    
class LoginApi(APIView):
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(username = serializer.data['username'],password = serializer.data['password'])
            if user is None:
                return Response({
                    "status":False,
                    "message":"username or password is wrong"
                },status=401)
            token,created = Token.objects.get_or_create(user = user)
            return Response({
                "status":True,
                "message":"Login Successfull",
                "data":token.key
            },status=200)