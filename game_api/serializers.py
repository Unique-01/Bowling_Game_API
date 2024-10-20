from rest_framework import serializers
from .models import Game, Roll


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'created_at', 'title', 'completed','rolls']
        read_only_fields = ['completed','rolls']


class RollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roll
        fields = ['id', 'game', 'frame', 'roll_number',
                  'knocked_down_pins', 'created_at']
