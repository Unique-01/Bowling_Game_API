from django.urls import path
from .views import GameView, GameRollView, GameScoreView, GameSummaryView

urlpatterns = [
    path("games/", GameView.as_view(), name="games"),
    path("games/<int:game_id>/rolls/", GameRollView.as_view(), name="rolls"),
    path("games/<int:game_id>/score/", GameScoreView.as_view(), name="score"),
    path(
        "games/<int:game_id>/summary/", GameSummaryView.as_view(), name="game_summary"
    ),
]
