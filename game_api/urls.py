from django.urls import path
from .views import GameView, GameRollView, GameScoreView, GameSummaryView

urlpatterns = [
    # Endpoint to create a new bowling game or list existing games
    path("games/", GameView.as_view(), name="games"),
    # Endpoint to record a roll for a specific game
    path("games/<int:game_id>/rolls/", GameRollView.as_view(), name="rolls"),
    # Endpoint to retrieve the current score of a specific game
    path("games/<int:game_id>/score/", GameScoreView.as_view(), name="score"),
    # Endpoint to get a natural language summary of the current game state
    path(
        "games/<int:game_id>/summary/", GameSummaryView.as_view(), name="game_summary"
    ),
]
