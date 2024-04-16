from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages
from violation.models import Vehicle

from violation.serializers import VehicleSerializer


class HomeView(TemplateView):
    template_name = "violation/home.html"

    def post(self, request):
        serializer = VehicleSerializer(data=request.POST)
        if not serializer.is_valid():
            errors = serializer.errors
            errors.pop("number_plate", None)
            if errors:
                messages.error(request, errors)

        Vehicle.objects.update_or_create(defaults=serializer.validated_data)
        messages.success(request, "Dang ky thanh cong")
        return redirect("/")
