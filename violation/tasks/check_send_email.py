from celery.app import shared_task
from phatnguoi import VehicleChecker
from core.tasks.send_email_task import send_mail_for_template
from violation.models import Vehicle
import re
from datetime import datetime
from django.db import transaction
import logging

DATETIME_FORMAT = "%H:%M, %d/%m/%Y"
logger = logging.getLogger(__name__)


@shared_task
# @transaction.atomic
def check_send_email():
    vehicles = Vehicle.objects.filter(email__isnull=False, type__isnull=False, number_plate__isnull=False)
    for vehicle in vehicles:
        number_plate = vehicle.number_plate
        logger.info(f"Check {number_plate}")
        vehicle_type = vehicle.type
        email = vehicle.email
        checker = VehicleChecker(number_plate, vehicle_type)
        result = checker.check()
        if not result:
            logger.info(f"Not found!")
            continue

        pattern = r"\d{2}:\d{2}, \d{2}/\d{2}/\d{4}"
        match = re.search(pattern, result.text)
        last_violation = vehicle.last_violation
        violation_time = datetime.strptime(match.group(), DATETIME_FORMAT) if match else None
        if violation_time != last_violation:
            vehicle.last_violation = violation_time
            vehicle.save()
        if not last_violation or violation_time and violation_time > last_violation.replace(tzinfo=None):
            base64_img = result.screenshot_as_base64
            context = {
                "image": base64_img
            }
            logger.info(f"Send to email {email} - {number_plate}")
            send_mail_for_template.delay(None, [email], "violation/email/notification", context)
