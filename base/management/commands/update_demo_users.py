from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Updates demo users to match the configured UNIVERSITY_EMAIL_DOMAIN (no posts/comments created)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Confirm updating demo users.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not options["yes"]:
            self.stdout.write(self.style.ERROR("Refusing to run without --yes"))
            self.stdout.write("This command updates demo user emails/passwords to match settings.")
            return

        from base.models import User

        domain = getattr(settings, "UNIVERSITY_EMAIL_DOMAIN", "th-deg.de").strip().lower()

        # Only touch known demo users by username to avoid modifying real users.
        demo_specs = [
            {
                "username": "student1",
                "email": f"student1@{domain}",
                "name": "Student One",
                "password": "student123",
                "affiliation": User.Affiliation.STUDENT,
            },
            {
                "username": "student2",
                "email": f"student2@{domain}",
                "name": "Student Two",
                "password": "student123",
                "affiliation": User.Affiliation.STUDENT,
            },
            {
                "username": "alumni1",
                "email": "alumni1@gmail.com",
                "name": "Alumni One",
                "password": "alumni123",
                "affiliation": User.Affiliation.ALUMNI,
            },
        ]

        for spec in demo_specs:
            username = spec["username"].lower()
            desired_email = spec["email"].lower()

            user = User.objects.filter(username=username).first()
            if user is None:
                # Fallback for older seed versions that keyed by email.
                user = User.objects.filter(email=desired_email).first()

            if user is None:
                # Create if missing.
                user = User.objects.create_user(
                    email=desired_email,
                    username=username,
                    password=spec["password"],
                )
            else:
                # Ensure unique email.
                conflict = User.objects.filter(email=desired_email).exclude(id=user.id).first()
                if conflict is not None:
                    raise RuntimeError(
                        f"Cannot set {username} email to {desired_email}: already used by user id={conflict.id}"
                    )

                user.email = desired_email
                user.username = username
                user.set_password(spec["password"])

            user.name = spec["name"]
            user.affiliation = spec["affiliation"]
            user.save(update_fields=["email", "username", "password", "name", "affiliation"])

        self.stdout.write(self.style.SUCCESS("Updated demo users."))
        for spec in demo_specs:
            self.stdout.write(f"- {spec['email']} / {spec['password']}")
