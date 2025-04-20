from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Person
from rest_framework import status

from .serializers import PersonSerializer,ColorSerializer,LoginSerializer,RegisterSerializer

from rest_framework.views import APIView


from rest_framework.viewsets import ModelViewSet 

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token






#DECORATOR API VIEW

@api_view(['GET',"POST"])
def index(request):
    courses ={
        'Name': 'python',
        'tools': {'drf','flask','fastapi'}

    }

    if request.method == "GET":
        print('it is a GET method')
        return Response(courses)
    elif request.method == "POST":
        print("GO POST")
        return Response(courses)



@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == "GET":
        obj = Person.objects.all()
        serializer = PersonSerializer(obj,many = True)
        return Response(serializer.data)
    

    elif request.method == "POST":
       
        serializer = PersonSerializer(data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == "PUT":
        data=request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj,data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == "PATCH":
        data = request.data
        obj = Person.objects.get(id=data['id'])

        serializer=PersonSerializer(obj,data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


    else:
        data = request.data 
        obj = Person.objects.get(id=data['id'])

        obj.delete()
        return Response({'message':'person deleted'})


@api_view(['POST'])
def login(request):
    data = request.data
    serializer=LoginSerializer(data=data)
    if serializer.is_valid():
        data = serializer.validated_data
        print(data)
        return Response({"successfull"})
      # Return this if validation fails
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Class Based API VIEW

class PersonApiView(APIView): 



    def get(self,request):
        obj = Person.objects.all()
        serializer = PersonSerializer(obj,many=True)
        return Response(serializer.data)
    def post(self,request):
        
        serializer = PersonSerializer(data= request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    def put(self,request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def patch(self,request):
        data = request.data 
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj,data,partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    


#Model ViewSET


class PersonViewset(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer



class RegsiterApiView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully created"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "message": "Login successful",
                    "token": token.key
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)