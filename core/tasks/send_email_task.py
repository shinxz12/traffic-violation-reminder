from celery.app import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_mail_for_template(from_email, recipient_list, template_without_ext, context, request=None, *args, **kwargs):
    subject = render_to_string('{}_subject.txt'.format(template_without_ext), context, request=request).strip()
    body_html = render_to_string('{}.html'.format(template_without_ext), context, request=request)
    body_text = render_to_string('{}.txt'.format(template_without_ext), context, request=request)
    return send_mail(subject, body_text, from_email, recipient_list, html_message=body_html, *args, **kwargs)
