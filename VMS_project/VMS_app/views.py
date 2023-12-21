from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, UpdateAPIView, RetrieveAPIView
from VMS_app.serializers import VendorSerializer, PurchaseOrderSerializer, AcknowledgeSerializer, PerformanceSerializer
from VMS_app.models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, F, ExpressionWrapper, fields
from django.db import transaction
from VMS_app.models import HistoricalPerformance, PurchaseOrder
from django.utils import timezone

# Create your views here.

# This is used to list all vendors or create a new vendor
class CreateVendorList(ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():

            return Response({"message": "No vendors found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)


# This is used to retrieve details or update a specific vendor
class UpdateVendor(RetrieveUpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

# This is used to retrieve details or delete a specific vendor
class DeleteVendor(RetrieveDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

# This is used to list all purchase orders or create a new purchase order
class CreatePurchaseOrderList(ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():

            return Response({"message": "No purchase order found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve details or update a specific purchase order
class UpdatePurchaseOrder(RetrieveUpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

# Retrieve details or delete a specific purchase order
class DeletePurchaseOrder(RetrieveDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)    

# Acknowledge the receipt of a purchase order
class AcknowledgeUpdate(UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = AcknowledgeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

# Retrieve performance details of a specific vendor
class VendorPerformance(RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = PerformanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

# below signal triggers performance calculation and updates in vendor and Historical performance model whenever changes made in Purchase order model.
@receiver(post_save, sender=PurchaseOrder)
def performace_update(sender, instance, **kwargs):
    vendor = instance.vendor
    print('vendor from instance', vendor)
    completed_pos = PurchaseOrder.objects.filter(
        vendor=vendor, status='Completed')
    total_completed_pos = completed_pos.count()
    print('total_completed_pos', total_completed_pos)
    # on-time delivery rate calculation in percentage

    on_time_delivery_rate = completed_pos.filter(vendor=vendor, delivery_date__lte=timezone.now(
    )).count()/total_completed_pos * 100 if total_completed_pos > 0 else 0.0

    # average quality rating calculation(1 to 5 rating)

    total_rating = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False).aggregate(
        avg_quality_rating=Avg('quality_rating', default=0.0))

    average_quality_rating = total_rating.get('avg_quality_rating', 0.0)

    # response time calculation in minutes

    acknowledged_pos = completed_pos.filter(
        vendor=vendor, acknowledgment_date__isnull=False)

    response_time = acknowledged_pos.filter(vendor=vendor).aggregate(avg_response_time=Avg(ExpressionWrapper(
        F("acknowledgment_date") - F("issue_date"),
        output_field=fields.DurationField())))

    average_response_time = response_time.get('avg_response_time', 0.0)

    # fulfillment rate calculation in percentage

    issued_pos_count = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfillment_rate = total_completed_pos / \
        issued_pos_count*100 if issued_pos_count else 0.0

    # Update Vendor model
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = average_quality_rating
    vendor.average_response_time = round(average_response_time.total_seconds() /
                                         60 if average_response_time else 0.0, 2)
    vendor.fulfillment_rate = fulfillment_rate

    vendor.save()

    # Update Performance model
    # transaction.atomic guarantees either the success of all operations or the complete rollback in case of any failure.
    with transaction.atomic():
        update_historical_performance = HistoricalPerformance.objects.create(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=average_quality_rating,
            average_response_time=round(average_response_time.total_seconds() /
                                        60 if average_response_time else 0.0, 2),
            fulfillment_rate=fulfillment_rate,

        )