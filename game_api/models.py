from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title or f"Game {self.id}"


class Roll(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='rolls')
    frame = models.IntegerField()
    roll_number = models.IntegerField()
    knocked_down_pins = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Roll {self.id}"
