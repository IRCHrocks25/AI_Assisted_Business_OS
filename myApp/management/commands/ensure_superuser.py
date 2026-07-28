"""Create or reset a Django superuser from environment variables.

Set on Railway:
  DJANGO_SUPERUSER_USERNAME
  DJANGO_SUPERUSER_PASSWORD
  DJANGO_SUPERUSER_EMAIL (optional)

Optional:
  DJANGO_SUPERUSER_RESET=1  → update password / staff flags if user already exists
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ensure a staff superuser exists from DJANGO_SUPERUSER_* env vars."

    def handle(self, *args, **options):
        username = (os.environ.get("DJANGO_SUPERUSER_USERNAME") or "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD") or ""
        email = (os.environ.get("DJANGO_SUPERUSER_EMAIL") or "").strip()
        reset = (os.environ.get("DJANGO_SUPERUSER_RESET") or "").strip() == "1"

        if not username or not password:
            self.stdout.write(
                "Skipping ensure_superuser (set DJANGO_SUPERUSER_USERNAME and "
                "DJANGO_SUPERUSER_PASSWORD on Railway to create an admin)."
            )
            return

        User = get_user_model()
        user = User.objects.filter(username=username).first()
        if user is None:
            User.objects.create_superuser(username=username, email=email or "", password=password)
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
            return

        if reset:
            user.set_password(password)
            if email:
                user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Reset superuser '{username}'."))
            return

        self.stdout.write(f"Superuser '{username}' already exists (set DJANGO_SUPERUSER_RESET=1 to update password).")
