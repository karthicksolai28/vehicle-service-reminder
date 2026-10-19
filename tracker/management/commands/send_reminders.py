from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth.models import User
from tracker.models import Vehicle


class Command(BaseCommand):
    help = 'Send service reminder emails to users'

    def handle(self, *args, **kwargs):
        sent = 0
        for user in User.objects.exclude(email=''):
            lines = []
            for v in Vehicle.objects.filter(user=user):
                if v.status == 'Overdue':
                    lines.append(f"- {v.name} ({v.number}): {abs(v.days_left)} days overdue")
                elif v.status == 'Due soon':
                    lines.append(f"- {v.name} ({v.number}): due in {v.days_left} days")

            if lines:
                message = f"Hi {user.username},\n\nService reminder:\n\n" + "\n".join(lines)
                send_mail('Vehicle Service Reminder', message, None, [user.email])
                sent += 1

        self.stdout.write(f"{sent} reminder email(s) sent.")