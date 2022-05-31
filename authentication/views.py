from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from authentication.models import CustomUser
import re
from authentication.serializers import UserSerializer
from rest_framework import status

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check_valid_email(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def check_unique_email(email):
    if CustomUser.objects.filter(email=email).exists():
        return True
    return False


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if email is None or email == '':
            return Response({'message': 'Email must be required'}, status=status.HTTP_400_BAD_REQUEST)

        if password1 is None or password2 is None:
            return Response({'message': 'Password must be required'}, status=status.HTTP_400_BAD_REQUEST)

        if password1 != password2:
            return Response({'message': 'Password not matched'}, status=status.HTTP_400_BAD_REQUEST)

        if check_valid_email(email):
            if check_unique_email(email):
                return Response({'message': "Email already exist in the system"}, status=status.HTTP_400_BAD_REQUEST)
            CustomUser.objects.create_user(email=email, password=password1)
            return Response({'message': 'User created successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid email provided'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request):
        user = CustomUser.objects.filter(id=request.user.id).first()
        if user is None:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        serialize = UserSerializer(user)
        return Response(serialize.data, status=status.HTTP_200_OK)
