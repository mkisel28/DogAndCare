from rest_framework import serializers

from apps.walks.models import Walk, WalkStats


class WalkSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(read_only=True)

    class Meta:
        model = Walk
        exclude = ["owner", "pet"]


class WalkStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkStats
        exclude = ["pet", "id"]
