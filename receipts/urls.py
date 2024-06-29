from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, ReceiptViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'receipts', ReceiptViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


"""

// Function to get the token
function getToken() {
    // Replace with your method of retrieving the token
    return localStorage.getItem('token');
}

// Confirm receipt
function confirmReceipt(receiptId) {
    fetch(`/api/receipts/${receiptId}/confirm/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken() // Replace getToken() with your method for getting the token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'receipt confirmed') {
            alert('Receipt confirmed successfully');
        } else {
            alert('Failed to confirm receipt: ' + data.status);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Reject receipt
function rejectReceipt(receiptId) {
    fetch(`/api/receipts/${receiptId}/reject/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken() // Replace getToken() with your method for getting the token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'receipt rejected') {
            alert('Receipt rejected successfully');
        } else {
            alert('Failed to reject receipt: ' + data.status);
        }
    })
    .catch(error => console.error('Error:', error));
}

"""