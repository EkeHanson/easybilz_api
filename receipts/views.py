# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Payment, Receipt
# from .serializers import PaymentSerializer, ReceiptSerializer

# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     # permission_classes = [IsAuthenticated]

# class ReceiptViewSet(viewsets.ModelViewSet):
#     queryset = Receipt.objects.all()
#     serializer_class = ReceiptSerializer
#     # permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
#     def confirm(self, request, pk=None):
#         try:
#             receipt = self.get_object()
#             if receipt.status == 'pending':
#                 receipt.status = 'confirmed'
#                 receipt.save()
#                 # Create payment record
#                 Payment.objects.create(
#                     user=receipt.user,
#                     amount=receipt.details.get('amount', 0),
#                     payment_method='Receipt Upload',
#                     transaction_id=receipt.receipt_number,
#                     status='completed'
#                 )
#                 return Response({'status': 'receipt confirmed'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'status': 'receipt not in pending state'}, status=status.HTTP_400_BAD_REQUEST)
#         except Receipt.DoesNotExist:
#             return Response({'status': 'receipt not found'}, status=status.HTTP_404_NOT_FOUND)

#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
#     def reject(self, request, pk=None):
#         try:
#             receipt = self.get_object()
#             if receipt.status == 'pending':
#                 receipt.status = 'rejected'
#                 receipt.save()
#                 return Response({'status': 'receipt rejected'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'status': 'receipt not in pending state'}, status=status.HTTP_400_BAD_REQUEST)
#         except Receipt.DoesNotExist:
#             return Response({'status': 'receipt not found'}, status=status.HTTP_404_NOT_FOUND)



from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Payment, Receipt
from registeration.models import CustomUser
from .serializers import PaymentSerializer, ReceiptSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    # permission_classes = [IsAuthenticated]

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print(serializer.errors)  # Log the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_payment_confirm_email(self, email, first_name, last_name):
        # Check if the email is linked to an existing account
        # if CustomUser.objects.filter(email=email).exists():
        #     return {'message': 'An account with this email already exists.'}

        if email:
            subject = 'Payment Confirmation'
            message = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Payment Confirmation</title>
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
                            <p>Congratulations on your successful payment to Easybillz Cooperative.<br> This email is a confirmation of your payment.</p>
                            <a href='https://easybilz-dzouisb3z-ekehansons-projects.vercel.app/?first_name={first_name}&last_name={last_name}&email={email}' class="button">Visit EasyBilz</a>
                            <p>If you did not request this payment, please ignore this email.</p>
                            <p>Thank you, <br>Easybillz Cooperative</p>
                        </div>
                    </div>
                </body>
                </html>
            '''
            recipient_list = [email]
            from_email = 'Do not reply <payment@easybilz.co.ng>'  # Set the no-reply email address

            try:
                result = send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=message)
                return {'message': 'Email sent successfully'}
            except Exception as e:
                return {'error': f'Failed to send email: {str(e)}'}
        else:
            return {'error': 'Email not provided'}

    # @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        try:
            receipt = self.get_object()
            if receipt.status == 'pending':
                receipt.status = 'confirmed'
                receipt.save()
                # Create payment record
                payment = Payment.objects.create(
                    user=receipt.user,
                    amount=20.43,
                    payment_method='Receipt Upload',
                    transaction_id=receipt.receipt_number,
                    status='completed'
                )

                # Send payment confirmation email
                email_response = self.send_payment_confirm_email(
                    email=receipt.user.email,
                    first_name=receipt.user.first_name,
                    last_name=receipt.user.last_name
                )

                if 'error' in email_response:
                    return Response({'status': 'receipt confirmed but email failed', 'error': email_response['error']}, status=status.HTTP_200_OK)

                return Response({'status': 'receipt confirmed and email sent'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'receipt not in pending state'}, status=status.HTTP_400_BAD_REQUEST)
        except Receipt.DoesNotExist:
            return Response({'status': 'receipt not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        try:
            receipt = self.get_object()
            if receipt.status == 'pending':
                receipt.status = 'rejected'
                receipt.save()
                return Response({'status': 'receipt rejected'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'receipt not in pending state'}, status=status.HTTP_400_BAD_REQUEST)
        except Receipt.DoesNotExist:
            return Response({'status': 'receipt not found'}, status=status.HTTP_404_NOT_FOUND)