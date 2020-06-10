from rest_framework import serializers


from .models import LoanInquiry


class LoanInquirySerializer(serializers.BaseSerializer):
    status = ""
    msg = ""

    def to_representation(self, instance):
        return {"status": instance.inquiry_approved, "msg": inquiry_rejected_because}
