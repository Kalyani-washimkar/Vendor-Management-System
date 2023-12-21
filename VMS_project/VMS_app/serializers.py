from rest_framework import serializers
from VMS_app.models import HistoricalPerformance, PurchaseOrder, Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code']

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.contact_details = validated_data.get('contact_details', instance.contact_details)
            instance.address = validated_data.get('address', instance.address)
            instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
            instance.save()
            return instance


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date',
                  'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']


class AcknowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['acknowledgment_date']


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg',
                  'average_response_time', 'fulfillment_rate']