from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.conf import settings


class Command(BaseCommand):
    help = "Seeds demo users, posts, comments, votes, and invite codes for local testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Confirm creating demo data.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not options["yes"]:
            self.stdout.write(self.style.ERROR("Refusing to run without --yes"))
            self.stdout.write("This command creates demo users, posts, comments, votes, and invite codes.")
            return

        from base.models import InvitationCode, Message, PostVote, Room, Topic, User

        student_domain = getattr(settings, 'UNIVERSITY_EMAIL_DOMAIN', 'th-deg.de').strip().lower()

        # --- Users (easy passwords) ---
        demo_users = [
            {
                "email": f"student1@{student_domain}",
                "username": "student1",
                "name": "Student One",
                "password": "student123",
                "affiliation": User.Affiliation.STUDENT,
            },
            {
                "email": f"student2@{student_domain}",
                "username": "student2",
                "name": "Student Two",
                "password": "student123",
                "affiliation": User.Affiliation.STUDENT,
            },
            {
                "email": "alumni1@gmail.com",
                "username": "alumni1",
                "name": "Alumni One",
                "password": "alumni123",
                "affiliation": User.Affiliation.ALUMNI,
            },
        ]

        created_users = {}
        for data in demo_users:
            user = User.objects.filter(email=data["email"].lower()).first()
            if user is None:
                user = User.objects.create_user(
                    email=data["email"].lower(),
                    username=data["username"].lower(),
                    password=data["password"],
                )
                user.name = data["name"]
                user.affiliation = data["affiliation"]
                user.save(update_fields=["name", "affiliation"])
            else:
                # Keep it predictable for testing
                user.username = data["username"].lower()
                user.name = data["name"]
                user.affiliation = data["affiliation"]
                user.set_password(data["password"])
                user.save(update_fields=["username", "name", "affiliation", "password"])

            created_users[data["username"]] = user

        student1 = created_users["student1"]
        student2 = created_users["student2"]
        alumni1 = created_users["alumni1"]

        # --- Invitation codes ---
        # One unused code you can try during alumni registration.
        InvitationCode.objects.get_or_create(code="ALUMNI2025", defaults={"is_active": True})

        # One code marked used (to test 'already used' validation).
        used_code = InvitationCode.objects.filter(code="ALUMNI2025USED").first()
        if used_code is None:
            used_code = InvitationCode.objects.create(code="ALUMNI2025USED", is_active=True)
        if used_code.used_at is None:
            used_code.used_at = timezone.now()
            used_code.used_by = alumni1
            used_code.save(update_fields=["used_at", "used_by"])

        # --- Topics (finite categories) ---
        def topic(slug: str) -> Topic:
            t = Topic.objects.filter(slug=slug).first()
            if t is None:
                raise RuntimeError(f"Missing Topic slug={slug}. Run migrations first.")
            return t

        # --- Posts (Rooms) ---
        posts = [
            {
                "topic": "exams-study",
                "host": student1,
                "title": "Need help with Finals: Data Structures",
                "body": "Anyone has good notes/practice sets for trees, heaps, and graphs? Happy to swap resources.",
            },
            {
                "topic": "exams-study",
                "host": student2,
                "title": "Study group for Calculus final?",
                "body": "If you're revising integration techniques and series, let's form a small study group this week.",
            },
            {
                "topic": "exams-study",
                "host": student1,
                "title": "Past papers for Operating Systems",
                "body": "Does anyone have past question papers for OS? Looking for scheduling + deadlocks practice.",
            },
            {
                "topic": "relocation",
                "host": student2,
                "title": "New to campus/city — tips for settling in?",
                "body": "Where do students usually find affordable groceries and how do you handle local transport?",
            },
            {
                "topic": "relocation",
                "host": student1,
                "title": "Best areas to live near campus",
                "body": "Any neighborhood suggestions (safe + affordable) for students commuting daily?",
            },
            {
                "topic": "relocation",
                "host": student2,
                "title": "First-week checklist for newcomers",
                "body": "What are the must-dos in the first week? SIM, ID card, bank, libraries—what did you miss?",
            },
            {
                "topic": "jobs-referrals",
                "host": alumni1,
                "title": "Hiring: Junior Backend Intern (referral possible)",
                "body": "My team is opening intern roles. Share your resume + GitHub. I can refer strong candidates.",
            },
            {
                "topic": "jobs-referrals",
                "host": alumni1,
                "title": "Resume review thread (post yours)",
                "body": "Drop your resume (anonymized) and role you're targeting. Seniors/alumni can give feedback.",
            },
            {
                "topic": "jobs-referrals",
                "host": student2,
                "title": "Interview prep: common HR questions",
                "body": "What questions did you get for internships or placements? Share your experience and tips.",
            },
            {
                "topic": "internships",
                "host": student1,
                "title": "How to land first internship with no experience?",
                "body": "What projects should I build? What matters most: GPA, projects, or referrals?",
            },
            {
                "topic": "internships",
                "host": student2,
                "title": "Internship timeline advice",
                "body": "When do companies usually open applications? Any calendar or strategy that worked for you?",
            },
            {
                "topic": "housing",
                "host": student1,
                "title": "Looking for a roommate near campus",
                "body": "2BR available from next month. Prefer quiet/clean. DM if interested.",
            },
            {
                "topic": "housing",
                "host": student2,
                "title": "Hostel vs flat: what did you choose?",
                "body": "Trying to decide between hostel and renting. Pros/cons based on your experience?",
            },
            {
                "topic": "housing",
                "host": student1,
                "title": "Budget furniture recommendations",
                "body": "Any good places to get a desk + chair cheaply? New or used is fine.",
            },
            {
                "topic": "events-clubs",
                "host": student2,
                "title": "Which clubs are active this semester?",
                "body": "Looking for recommendations: tech, music, photography, volunteering—what's worth joining?",
            },
            {
                "topic": "events-clubs",
                "host": student1,
                "title": "Anyone going to the cultural fest?",
                "body": "Planning to attend. Would love to go as a group and meet people from other departments.",
            },
            {
                "topic": "buy-sell",
                "host": student1,
                "title": "Selling: used textbooks (CS + Math)",
                "body": "Selling a few textbooks in good condition. DM what you need and I’ll share prices.",
            },
            {
                "topic": "buy-sell",
                "host": student2,
                "title": "Need: second-hand bicycle",
                "body": "Looking for a used bicycle for commuting. Any leads or sellers?",
            },
            {
                "topic": "admin-paperwork",
                "host": student2,
                "title": "Help: scholarship / fee waiver process",
                "body": "Which documents are required and where do we submit? Any common mistakes to avoid?",
            },
            {
                "topic": "admin-paperwork",
                "host": student1,
                "title": "Transcript / bonafide certificate timeline",
                "body": "How long does it usually take to get transcripts or bonafide certificate issued?",
            },
            {
                "topic": "wellbeing",
                "host": student2,
                "title": "Feeling overwhelmed this semester",
                "body": "Any study routines or campus resources you recommend? Want to improve without burning out.",
            },
            {
                "topic": "wellbeing",
                "host": student1,
                "title": "Balancing part-time work and classes",
                "body": "If you're working part-time, how do you manage assignments and sleep? Tips appreciated.",
            },
            {
                "topic": "wellbeing",
                "host": alumni1,
                "title": "Burnout prevention: what worked for me",
                "body": "Short routine + prioritization tips I used during final year. Sharing in case it helps.",
            },
            {
                "topic": "tech-projects",
                "host": student1,
                "title": "Project buddy for a hackathon?",
                "body": "Looking for 1–2 teammates for a weekend hackathon. Web + Python preferred.",
            },
            {
                "topic": "tech-projects",
                "host": student2,
                "title": "Code review for my Django project",
                "body": "Built a small Django app. Would love feedback on structure, security, and deployment.",
            },
            {
                "topic": "tech-projects",
                "host": alumni1,
                "title": "Open-source starter ideas for students",
                "body": "If you're new to OSS, here are beginner-friendly project ideas you can build with others.",
            },
            {
                "topic": "alumni-network",
                "host": alumni1,
                "title": "Alumni AMA: ask me anything about placements",
                "body": "Happy to answer questions about preparation, interviews, and what companies look for.",
            },
            {
                "topic": "alumni-network",
                "host": student1,
                "title": "Seeking alumni mentor for career guidance",
                "body": "Looking for a mentor in software/data. 15 min chat weekly would help a lot.",
            },
            {
                "topic": "other",
                "host": student2,
                "title": "Best campus food spots?",
                "body": "Where do you eat on/near campus? Looking for budget-friendly and tasty options.",
            },
            {
                "topic": "other",
                "host": student1,
                "title": "General tips for first-year students",
                "body": "What do you wish you knew in first year? Share advice for academics and campus life.",
            },
        ]

        created_rooms = {}
        for p in posts:
            t = topic(p["topic"])

            room = Room.objects.filter(host=p["host"], topic=t, name=p["title"]).first()
            if room is None:
                room = Room.objects.create(
                    host=p["host"],
                    topic=t,
                    name=p["title"],
                    description=p["body"],
                )
            else:
                room.description = p["body"]
                room.save(update_fields=["description"])

            created_rooms[p["title"]] = room

        # --- Comments (Messages) + participants ---
        def comment(room_title: str, user: User, text: str):
            room = created_rooms[room_title]
            msg = Message.objects.create(user=user, room=room, body=text)
            room.participants.add(user)
            return msg

        comment(
            "Need help with Finals: Data Structures",
            student2,
            "I have a good set of graph problems. Want me to share a link?",
        )
        comment(
            "Need help with Finals: Data Structures",
            alumni1,
            "For graphs: practice BFS/DFS + shortest path patterns. Happy to suggest resources.",
        )

        comment(
            "New to campus/city — tips for settling in?",
            student1,
            "Join 1–2 clubs early. It helps a lot with meeting people.",
        )

        comment(
            "Hiring: Junior Backend Intern (referral possible)",
            student1,
            "Thanks! What stack is the team using?",
        )
        comment(
            "Hiring: Junior Backend Intern (referral possible)",
            alumni1,
            "Mostly Django + Postgres + some AWS. Basics are enough for interns.",
        )

        comment(
            "Resume review thread (post yours)",
            student1,
            "Should we also share a template format that works well for ATS?",
        )
        comment(
            "Study group for Calculus final?",
            student1,
            "I'm in. Which chapters are you focusing on?",
        )
        comment(
            "Alumni AMA: ask me anything about placements",
            student2,
            "What’s the best way to prepare for coding rounds if time is limited?",
        )

        # --- Votes ---
        def vote(room_title: str, user: User, value: int):
            room = created_rooms[room_title]
            PostVote.objects.update_or_create(user=user, room=room, defaults={"value": value})

        vote("Need help with Finals: Data Structures", student2, 1)
        vote("Need help with Finals: Data Structures", alumni1, 1)

        vote("New to campus/city — tips for settling in?", student1, 1)

        vote("Hiring: Junior Backend Intern (referral possible)", student1, 1)
        vote("Hiring: Junior Backend Intern (referral possible)", student2, 1)
        vote("Hiring: Junior Backend Intern (referral possible)", alumni1, 1)

        vote("Feeling overwhelmed this semester", student1, 1)
        vote("Feeling overwhelmed this semester", alumni1, 1)

        vote("Resume review thread (post yours)", student2, 1)
        vote("Resume review thread (post yours)", alumni1, 1)

        vote("Alumni AMA: ask me anything about placements", student1, 1)
        vote("Alumni AMA: ask me anything about placements", student2, 1)
        vote("Alumni AMA: ask me anything about placements", alumni1, 1)

        vote("Selling: used textbooks (CS + Math)", student2, 1)
        vote("Need: second-hand bicycle", student1, 1)

        self.stdout.write(self.style.SUCCESS("Seeded demo data."))
        self.stdout.write("\nDemo users:")
        for data in demo_users:
            self.stdout.write(f"- {data['email']} / {data['password']}")
        self.stdout.write("\nInvitation codes:")
        self.stdout.write("- ALUMNI2025 (unused)")
        self.stdout.write("- ALUMNI2025USED (already used)")
