from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Deletes all posts (rooms), comments (messages), and votes. Keeps users and categories."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Confirm destructive deletion.",
        )

    def handle(self, *args, **options):
        if not options["yes"]:
            self.stdout.write(self.style.ERROR("Refusing to run without --yes"))
            self.stdout.write("This command deletes ALL posts, comments, and votes.")
            return

        from base.models import Message, PostVote, Room

        vote_count = PostVote.objects.count()
        message_count = Message.objects.count()
        room_count = Room.objects.count()

        # Order matters to avoid FK issues.
        PostVote.objects.all().delete()
        Message.objects.all().delete()
        Room.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted rooms={room_count}, messages={message_count}, votes={vote_count}."
            )
        )
