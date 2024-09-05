from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response

from payment.models import Payment
from payment.serializers import PaymentSerializer
from payment.services import pay, get_session_info
from payment.views_docs_data import payment_retrieve_API_view_example


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        payment.session_id, payment.payment_url = pay(payment.amount)
        payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    @extend_schema(examples=payment_retrieve_API_view_example)
    def get(self, request, *args, **kwargs):
        obj = self.retrieve(request, *args, **kwargs)
        session_id = obj.data.get("session_id")
        stat = status.HTTP_200_OK
        data = get_session_info(session_id)
        return Response(data, status=stat)
