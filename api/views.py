from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .serializers import LoanInquirySerializer

from .API_request import create_new_inquiry


# Create your views here.
@api_view(["GET", "POST"])
def validate_IIN(request):
    if request.method == "POST":
        return Response(create_new_inquiry(request.data["IIN"], request.data["amount"]))
    return Response({"message": "Nothing is there"})
