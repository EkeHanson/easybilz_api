from django.contrib import admin
from .models import Payment, Receipt

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'payment_method', 'transaction_id', 'status')
    search_fields = ('user__email', 'transaction_id')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'receipt_number', 'issued_date', 'status')
    search_fields = ('user__email', 'receipt_number')
    actions = ['confirm_receipt', 'reject_receipt']

    def confirm_receipt(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_receipt.short_description = "Confirm selected receipts"

    def reject_receipt(self, request, queryset):
        queryset.update(status='rejected')
    reject_receipt.short_description = "Reject selected receipts"
