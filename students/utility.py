import requests
from rest_framework.response import Response
from rest_framework import status
from .models import FeePayment

def send_webhook_notification(webhook_url, request):
    reference :dict = request.GET.get("reference", None)

    fee = FeePayment.objects.filter(payment_ref_no=reference).first()
    if fee is None:
        return Response({"message": "FeePayment not found for the provided reference."}, status=status.HTTP_404_NOT_FOUND)
    headers = {'Content-Type': 'application/json'}
    data = {
        'message': 'Transaction was successful', 
        "fee_payment_id": fee.id,
        "user_id": fee.user_id,
        "fee_id": fee.fees_id,
        "reference": fee.payment_ref_no,
        "payment_status": fee.payment_status,
        }     
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code == 200:
        return {"message": "Payment was successful!", "status":"success", "data":data}
    return None
