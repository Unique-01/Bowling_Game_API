from rest_framework import serializers
from .models import Game, Roll


class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Game model.

    This serializer handles the validation and serialization of Game instances.
    It includes the following fields:
        - id: The unique identifier of the game (read-only).
        - created_at: The timestamp when the game was created (read-only).
        - title: The title of the game, optional.
        - completed: Indicates whether the game has been completed (read-only).
    """
    class Meta:
        model = Game
        fields = ["id", "created_at", "title", "completed"]
        read_only_fields = ["completed"]


class RollSerializer(serializers.ModelSerializer):
    """
    Serializer for the Roll model.

    This serializer manages the validation and serialization of Roll instances.
    It includes the following fields:
        - id: The unique identifier of the roll (read-only).
        - game: A foreign key reference to the associated Game instance.
        - frame: The frame number of the roll (1 to 10).
        - roll_number: The number of the roll within the frame (1, 2, or 3).
        - knocked_down_pins: The number of pins knocked down in this roll.
        - created_at: The timestamp when the roll was recorded (read-only).
    """
    class Meta:
        model = Roll
        fields = [
            "id",
            "game",
            "frame",
            "roll_number",
            "knocked_down_pins",
            "created_at",
        ]
