from rest_framework import serializers

from apps.robots.models import Robot


class RobotCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Robot
        fields = ['model', 'version', 'serial', 'created']

    def create(self, validated_data):
        return Robot.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RobotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']
