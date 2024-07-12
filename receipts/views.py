from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        # Save the receipt first
        receipt = serializer.save(user=self.request.user)

        # Generate the dynamic URL for the receipt file
        receipt_file_url = self.request.build_absolute_uri(receipt.upload.url) if receipt.upload else ''

        # Print the dynamic URL (for debugging purposes)
        print(receipt_file_url)

        # Send the payment confirmation email
        email_response = self.send_payment_confirm_email(
            email=receipt.user.email,
            first_name=self.request.user.firstName,
            last_name=self.request.user.otherNames,
            receipt_file_url=receipt_file_url
        )

        # Handle email sending errors
        if 'error' in email_response:
            # Optionally log the error or handle it as needed
            print(email_response['error'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print(serializer.errors)  # Log the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_payment_confirm_email(self, email, first_name, last_name, receipt_file_url):
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
                            <h3>Hi Admin,</h3>
                            <p>{first_name} {last_name} with the email {email} has successfully made payment to Easybillz Cooperative account.<br> Please
                            confirm receipt of the payment.</p>
                            <img src="{receipt_file_url}" alt="Receipt Image" width="400">
                            <p>If you did not receive any payment, please ignore this email.</p>
                            <p>Thank you, <br>Easybillz Cooperative Dev. Team</p>
                        </div>
                    </div>
                </body>
                </html>
            '''
            recipient_list = ["eazybillzcoop@gmail.com"]
            #recipient_list = ["ekenehanson@gmail.com"]
            from_email = recipient_list[0]  # Set the no-reply email address

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
