from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    class Affiliation(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        ALUMNI = 'ALUMNI', 'Alumni'

    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    affiliation = models.CharField(
        max_length=20,
        choices=Affiliation.choices,
        default=Affiliation.STUDENT,
    )
    # Demo paid flag (no real payments). Used to gate premium-only categories.
    is_paid = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class InvitationCode(models.Model):
    code = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_invite_codes',
    )
    used_at = models.DateTimeField(null=True, blank=True)
    used_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='used_invite_code',
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Topic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    name = models.TextField()
    description = models.TextField(null= True, blank= True)
    participants = models.ManyToManyField(User, related_name='participants', blank= True)
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class PostVote(models.Model):
    class Value(models.IntegerChoices):
        DOWN = -1, 'Downvote'
        UP = 1, 'Upvote'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='votes')
    value = models.IntegerField(choices=Value.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'room'], name='unique_post_vote'),
        ]

    def __str__(self):
        return f"{self.user_id}:{self.room_id}:{self.value}"
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]