from django.db import migrations
from django.utils.text import slugify


DEFAULT_CATEGORIES = [
    ("exams-study", "Exams & Study Help"),
    ("relocation", "Moving & Settling In"),
    ("jobs-referrals", "Jobs & Referrals"),
    ("internships", "Internships"),
    ("housing", "Housing & Roommates"),
    ("events-clubs", "Events & Clubs"),
    ("buy-sell", "Buy & Sell"),
    ("wellbeing", "Wellbeing & Mental Health"),
    ("admin-paperwork", "Admin & Paperwork"),
    ("tech-projects", "Tech & Projects"),
    ("alumni-network", "Alumni Network"),
    ("other", "Other"),
]


def _unique_slug(Topic, base_slug: str) -> str:
    slug = base_slug
    suffix = 2
    while Topic.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{suffix}"
        suffix += 1
    return slug


def seed_categories(apps, schema_editor):
    Topic = apps.get_model("base", "Topic")

    # Backfill slugs for any existing topics that don't have them.
    for topic in Topic.objects.filter(slug__isnull=True):
        base_slug = slugify(topic.name) or "category"
        topic.slug = _unique_slug(Topic, base_slug)
        topic.save(update_fields=["slug"])

    # Ensure default finite categories exist.
    for slug, name in DEFAULT_CATEGORIES:
        Topic.objects.get_or_create(slug=slug, defaults={"name": name})


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_topic_slug_user_affiliation_invitationcode_postvote"),
    ]

    operations = [
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
