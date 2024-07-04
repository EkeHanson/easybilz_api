from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import CustomUserSerializer
from .models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import Http404
from .serializers import LoginSerializer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import secrets
import datetime
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import CustomUser


# views.py
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        interest_of_service = data.get('interest_of_service')
        message = data.get('message')
       
        subject = interest_of_service
        full_message = f'''
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Registration Confirmation</title>
                            <style>
                                /* Define your CSS styles here */
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="header">
                                    <img src="https://artstraining.co.uk/img/site-logo.png" alt="Arts Training Logo" width="150">
                                </div>
                                <div class="content">
                                    <h3>Name: {name},<h3/>
                                    <h3>Email: {email},<h3/>
                                    <h3>Phone: {phone},<h3/>
                                    <h3>Subject: {interest_of_service},<h3/>
                                    <p>{message}</p>
                                </div>
                            </div>
                        </body>
                        </html>
                    '''

        recipients = ['info@artstraining.co.uk', 'support@artstraining.co.uk', 'ekehanson@gmail.com', 'abraham.h@turing.com']
        send_mail(subject, full_message, email, recipients, html_message=full_message)

        return JsonResponse({'status': 'success'}, status=201)
    return JsonResponse({'status': 'fail'}, status=400)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        remember_me = serializer.validated_data.get('remember_me', False)

        user = authenticate(email=email, password=password)

        if user:
            # If authentication is successful, generate JWT tokens
            refresh = RefreshToken.for_user(user)

            # Set token lifetime based on remember_me
            if remember_me:
                refresh.set_exp(lifetime=timedelta(days=14))  # Extend token expiration to 2 weeks
            else:
                refresh.set_exp(lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

            response_data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user_id': user.id,
                'user_email': user.email,
                'firstName': user.firstName,
                'middleName': user.middleName,
                'otherName': user.otherNames,
            }
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(response_data)


@api_view(['POST'])
def send_registration_email(request):
    if request.method == 'POST':
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        
        # Check if the email is linked to an existing account
        if CustomUser.objects.filter(email=email).exists():
            return Response({'message': 'An account with this email already exists.'})
        
        if email:
            subject = 'Registration Confirmation'
            message = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Registration Confirmation</title>
                    <style>
                        /* Define your CSS styles here */
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h3>Welcome to The Arts Training</h3>
                            <img src="https://artstraining.co.uk/img/site-logo.png" alt="Arts Training Logo" width="150">
                        </div>
                        <div class="content">
                            <h3>Hi {first_name},<h3/>
                            <p>Thank you for signing up with A.R.T.S Training.<br> Please click the link below to complete your registration.</p>
                            <a href='https://artstraining.co.uk/complete-signup.html?first_name={first_name}&last_name={last_name}&email={email}' class="button">Complete Registration</a>
                            <p>If you did not request for this registration, please ignore this email.</p>
                            <p>Thank you, <br> The Arts Training Team</p>
                        </div>
                    </div>
                </body>
                </html>
            '''

            recipient_list = [email]
            from_email = 'Do not reply <admin@artstraining.co.uk>'  # Set the no-reply email address
            try:
                result = send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=message)
                return Response({'message': result})
            except Exception as e:
                return Response({'error': f'Failed to send email: {str(e)}'}, status=500)
        else:
            return Response({'error': 'Email not provided in POST data'}, status=400)
    else:
        return Response({'error': 'Invalid request method'}, status=400)




class JWTExampleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'You are authenticated'}
        return Response(content)

class CreateUserAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print("Created a User!")

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            response_data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user_id': user.id,
                'user_email': user.email,
                'firstName': user.firstName,
                'middleName': user.middleName,
                'otherName': user.otherNames,
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        print("Serializer Error")
        print(serializer.errors)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    """
    API view to handle retrieving, updating, or deleting a single instructor.
    """

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve an existing instructor.
        """
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an existing instructor.
        """
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print("serializer.errors")
        print(serializer.errors)
        print("serializer.errors")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update an existing instructor.
        """
        print(request.data)
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print("serializer.errors")
        print(serializer.errors)
        print("serializer.errors")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        """
        Update an existing instructor.
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
def generate_reset_token():
    return secrets.token_urlsafe(16)

def send_reset_email(user):
    
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    print(user.reset_token)
    user.reset_token_expires = timezone.now() + datetime.timedelta(hours=10)  # Token expires in 3 hours
    user.save()
    reset_url = f'https://artstraining.co.uk/forgot-password-main.html?reset_token={reset_token}&amp;email={user.email}'
    
    subject = 'Password Reset'
    
    message =  f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Confirmation</title>
    <style>
        /* Define your CSS styles here */
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .content {{
            padding: 20px;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #87ceeb;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h3>Welcome to The Arts Training</h3>
            <img src="https://artstraining.co.uk/img/site-logo.png" alt="Arts Training Logo" width="150">
        </div>
        <div class="content">
            <h3>Hi {user.first_name},<h3/>
            <br>
            <a href='{reset_url}' class="button">Click this link to reset your password</a>
            <p>This link will expire in 1 hour</p>
        </div>
    </div>
</body>
</html>'''

    from_email = 'Do not reply'  # Update with your email address
    recipient_list = [user.email]  # Send email to the user's email address

    send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=message)

class PasswordResetAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned:
            return Response({'error': 'Multiple users found with this email'}, status=status.HTTP_400_BAD_REQUEST)
        
        send_reset_email(user)
        return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)

class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        reset_token = request.data.get('reset_token')
        email = request.data.get('email')
        password = request.data.get('password')

        # Retrieve the user based on the reset_token and email
        try:
            user = CustomUser.objects.get(email=email, reset_token=reset_token)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid reset token or email'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the reset token is expired
        if user.reset_token_expires < timezone.now():
            return Response({'error': 'Reset token has expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(password)
        user.reset_token = None
        user.reset_token_expires = None
        user.save()

        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)