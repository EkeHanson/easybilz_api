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




from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment, Receipt
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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        try:
            receipt = self.get_object()
            if receipt.status == 'pending':
                receipt.status = 'confirmed'
                receipt.save()
                # Create payment record
                Payment.objects.create(
                    user=receipt.user,
                    amount=receipt.details.get('amount', 0),
                    payment_method='Receipt Upload',
                    transaction_id=receipt.receipt_number,
                    status='completed'
                )
                return Response({'status': 'receipt confirmed'}, status=status.HTTP_200_OK)
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
