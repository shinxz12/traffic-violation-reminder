from celery.app import shared_task
from django.core.mail import send_mail
from phatnguoi import VehicleChecker
from core.tasks.send_email_task import send_mail_for_template
from violation.models import Vehicle


@shared_task
def check_send_email():
    vehicles =Vehicle.objects.filter(email__isnull=False, type__isnull=False, number_plate__isnull=False)
    for vehicle in vehicles:
        number_plate = vehicle.number_plate
        vehicle_type = vehicle.type
        email = vehicle.email
        checker = VehicleChecker(number_plate, vehicle_type)
        result = checker.check()
        if result:
            base64_img = result.screenshot_as_base64
            context = {
                "image": base64_img
            }
            send_mail_for_template.delay("a@gmail.com", [email], "violation/email/notification", context)
