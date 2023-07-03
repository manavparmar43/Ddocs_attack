import socket
from django.utils import timezone
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from Ddocs.models import User, RequestedAttempts
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserRegisterSerializer, MyTokenObtainPairSerializer, UserSerializer

class LoginViewApi(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserCreateViewApi(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        user_data=[{"username":request.data.get('username'),
                "password":request.data.get('password'),
                "email":request.data.get('email'),
                "first_name":request.data.get('first_name'),
                "last_name":request.data.get('last_name'),
                "ip_address":IPAddr
                }]
        serializer=UserRegisterSerializer(data=user_data,many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"data":serializer.data})
        else:
            return JsonResponse({"Error":serializer.errors})
    

class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        if request.user in users:
            if not request.user.permanent_blocked:
                if request.user.blocked_user == False:
                    hostname = socket.gethostname()
                    IPAddress = socket.gethostbyname(hostname)
                    requested_attempt = RequestedAttempts.objects.create(user=request.user, ip_address=IPAddress)
                    requested_attempts_of_user = RequestedAttempts.objects.filter(user=request.user, created_at__gte=timezone.now() - timezone.timedelta(seconds=20))
                    if len(requested_attempts_of_user) > 10:
                        request.user.blocked_user = True
                        request.user.save()
                        return Response({"400":"Bad Request, you are blocked for 20 minutes, you can try after 20 minutes!"})
                    else:
                        serializer = UserSerializer(users, many=True)
                        return Response(serializer.data)
                else:
                    hostname = socket.gethostname()
                    IPAddress = socket.gethostbyname(hostname)
                    new_requested_attempt = RequestedAttempts.objects.create(user=request.user, ip_address=IPAddress)
                    requested_attempt = RequestedAttempts.objects.filter(user=request.user).order_by("-id")
                    if requested_attempt[10].created_at >= (timezone.now() - timezone.timedelta(minutes=20)):
                        request.user.blocked_user = False
                        request.user.save()
                        return Response({"success":"You are unblocked and you can try again to access an API"})
                    elif (len(requested_attempt.filter(created_at__gte=(timezone.now() - timezone.timedelta(minutes=1)))) > 100):
                        request.user.permanent_blocked = True
                        request.user.save()
                        return Response({"400":"Permanently blocked !"})
                    return Response({"400":"Bad Request!"})
            else:
                return Response({"400":"Bad Request, You are permanently blocked !"})
        else:
            return Response({"authntication error":"login to get access!"})
