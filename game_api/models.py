from django.db import models


class Game(models.Model):
    """
    Represents a bowling game.

    Attributes:
        title (str): The title of the game, optional.
        created_at (datetime): The timestamp when the game was created.
        completed (bool): Indicates whether the game has been completed.
    """

    title = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        """Return a string representation of the Game instance."""
        return self.title or f"Game {self.id}"


class Roll(models.Model):
    """
    Represents a roll in a bowling game.

    Attributes:
        game (Game): A foreign key reference to the associated Game instance.
        frame (int): The frame number of the roll (1 to 10).
        roll_number (int): The number of the roll within the frame (1 or 2, or 3 for a strike).
        knocked_down_pins (int): The number of pins knocked down in this roll.
        created_at (datetime): The timestamp when the roll was recorded.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="rolls")
    frame = models.IntegerField()
    roll_number = models.IntegerField()
    knocked_down_pins = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Roll instance."""
        return f"Roll {self.id}"
