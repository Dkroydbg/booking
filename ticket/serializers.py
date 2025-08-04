from rest_framework import serializers
from .models import Event,Booking,Ticket
from .validators import no_numbers
from django.contrib.auth.models import User

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def run_validation(self, data=serializers.empty):
        if isinstance(data,dict):
            allowed = set(self.fields.keys())
            received = set(data.keys())
            extra = received-allowed
            if extra:
                raise serializers.ValidationError({field: 'This field is not allowed.' for field in extra})
        return super().run_validation(data)
    
    def validate_title(self,value):
        if Event.objects.filter(title=value).exists():
            raise serializers.ValidationError("Cannot have multiple events with the same title", value)
        return value
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['total_price']

    def run_validation(self, data=serializers.empty):
        allowed = set(self.fields.keys())
        received = set(data.keys())
        extra = received-allowed
        if extra:
            raise serializers.ValidationError({field: 'This field is not allowed.' for field in extra})
        return super().run_validation(data)
    

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def run_validation(self, data=serializers.empty):
        allowed = set(self.fields.keys())
        received = set(data.keys())
        extra = received-allowed
        if extra:
            raise serializers.ValidationError({field: 'This field is not allowed.' for field in extra})
        return super().run_validation(data)
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100,validators=[no_numbers])
    password = serializers.CharField(max_length=250,required=True)
    first_name = serializers.CharField(max_length=255,required=True)
    last_name = serializers.CharField(max_length=255,required=True)
    email = serializers.EmailField()

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self,value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("email already exists")
        return value
    def run_validation(self, data=serializers.empty):
        if isinstance(data,dict):
            allowed = set(self.fields.keys())
            received = set(data.keys())
            extra = received-allowed
            if extra:
                raise serializers.ValidationError({field: 'This field is not allowed.' for field in extra})
        return super().run_validation(data)
    
    def create(self,validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']

        user = User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
        return user
