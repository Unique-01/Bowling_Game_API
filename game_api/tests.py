from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Game, Roll


class GameAPITestCase(APITestCase):
    def setUp(self):
        """Set up the initial data for testing."""
        self.game = Game.objects.create(completed=False)
        self.roll_data = {"knocked_down_pins": 5}

    def test_list_games(self):
        """Test listing games."""
        response = self.client.get(reverse("games"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_game(self):
        """Test creating a new game."""
        response = self.client.post(reverse("games"), {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 2)

    def test_submit_roll_for_existing_game(self):
        """Test submitting a roll for an existing game."""
        response = self.client.post(
            reverse("rolls", args=[self.game.id]), self.roll_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Roll.objects.count(), 1)

    def test_submit_roll_for_completed_game(self):
        """Test submitting a roll for a completed game."""
        self.game.completed = True
        self.game.save()
        response = self.client.post(
            reverse("rolls", args=[self.game.id]), self.roll_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Game is already completed")

    def test_submit_roll_for_nonexistent_game(self):
        """Test submitting a roll for a nonexistent game."""
        response = self.client.post(
            reverse("rolls", args=[999]), self.roll_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Game not found")

    def test_submit_invalid_roll(self):
        """Test submitting an invalid roll (e.g., too many knocked down pins)."""
        self.roll_data["knocked_down_pins"] = 15  # Invalid input
        response = self.client.post(
            reverse("rolls", args=[self.game.id]), self.roll_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid knocked_down_pins value", response.data["error"])

    def test_get_score_for_existing_game(self):
        """Test retrieving the score for an existing game."""
        Roll.objects.create(game=self.game, frame=1, roll_number=1, knocked_down_pins=5)
        Roll.objects.create(game=self.game, frame=1, roll_number=2, knocked_down_pins=3)
        response = self.client.get(reverse("score", args=[self.game.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["score"], 8)

    def test_get_score_for_nonexistent_game(self):
        """Test getting the score for a nonexistent game."""
        response = self.client.get(reverse("score", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Game not found")

    def test_generate_game_summary(self):
        """Test generating a summary for an existing game."""
        Roll.objects.create(game=self.game, frame=1, roll_number=1, knocked_down_pins=5)
        Roll.objects.create(game=self.game, frame=1, roll_number=2, knocked_down_pins=3)
        response = self.client.get(reverse("game_summary", args=[self.game.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("summary", response.data)

    def test_generate_summary_for_nonexistent_game(self):
        """Test generating a summary for a nonexistent game."""
        response = self.client.get(reverse("game_summary", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Game not found")


if __name__ == "__main__":
    import unittest

    unittest.main()
