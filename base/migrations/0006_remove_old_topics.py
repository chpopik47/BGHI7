from django.db import migrations


ALLOWED_SLUGS = {
    "exams-study",
    "relocation",
    "jobs-referrals",
    "internships",
    "housing",
    "events-clubs",
    "buy-sell",
    "wellbeing",
    "admin-paperwork",
    "tech-projects",
    "alumni-network",
    "other",
}


def cleanup_topics(apps, schema_editor):
    Topic = apps.get_model("base", "Topic")
    Room = apps.get_model("base", "Room")

    other = Topic.objects.filter(slug="other").first()
    if other is None:
        other = Topic.objects.create(name="Other", slug="other")

    old_topics = Topic.objects.exclude(slug__in=ALLOWED_SLUGS)

    # Reassign rooms that still point to old topics
    for topic in old_topics:
        Room.objects.filter(topic=topic).update(topic=other)

    old_topics.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0005_seed_categories_and_slugs"),
    ]

    operations = [
        migrations.RunPython(cleanup_topics, migrations.RunPython.noop),
    ]
