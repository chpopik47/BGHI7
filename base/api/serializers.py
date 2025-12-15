from rest_framework import serializers

from base.models import Room, Topic, User


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "slug"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "affiliation", "is_paid"]


class RoomSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "host",
            "topic",
            "name",
            "description",
            "participants",
            "updated",
            "created",
        ]
