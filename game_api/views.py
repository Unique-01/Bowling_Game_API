from rest_framework import views
from rest_framework import generics
from .serializers import GameSerializer, RollSerializer
from .models import Game, Roll
from rest_framework.response import Response
from rest_framework import status
from .services import calculate_score, generate_game_summary


class GameView(generics.ListCreateAPIView):
    """
    API view to retrieve and create games.

    This view supports GET requests to list all games
    and POST requests to create a new game.
    """

    serializer_class = GameSerializer
    queryset = Game.objects.all()


class GameRollView(views.APIView):
    """
    API view to handle roll submissions for a specific game.

    This view allows players to submit their knocked down pins for a roll.
    It also calculates the current frame and determines if the game is complete.
    """

    def post(self, request, game_id):
        """
        Submit a roll for a specific game.

        Parameters:
            request (Request): The HTTP request object containing the roll data.
            game_id (int): The ID of the game.

        Returns:
            Response: The response object with the roll data or an error message.
        """
        # Response to be sent if game is already completed.
        game_completed_response = Response(
            {"error": "Game is already completed"}, status=status.HTTP_400_BAD_REQUEST
        )

        # Retrieve the game or return an error if it doesn't exist
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # If the game is completed, return an error response
        if game.completed:
            return game_completed_response

        # Retrieve knocked_down_pins from the request body
        knocked_down_pins = request.data.get("knocked_down_pins")

        # Check if knocked_down_pins is provided in the request
        if knocked_down_pins is None:
            return Response(
                {"error": "knocked_down_pins is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            

        # Validate knocked_down_pins
        if (
            not isinstance(knocked_down_pins, int) or
            knocked_down_pins < 0
            or knocked_down_pins > 10
        ):
            return Response(
                {
                    "error": f"Invalid knocked_down_pins value. It must be an integer between 0 and 10.{knocked_down_pins}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch all rolls in database ordered by creation time
        rolls = game.rolls.all().order_by("created_at")

        # Initialize current_frame and roll_number variable
        current_frame = 1
        roll_number = None

        # Determine the current frame by looping through rolls
        i = 0
        while i < len(rolls):
            roll = rolls[i]

            if current_frame < 10:
                if roll.knocked_down_pins == 10:
                    current_frame += 1
                else:
                    i += 1  # Go to the next roll for this frame
                    if i < len(rolls):
                        current_frame += 1
            else:
                frame_rolls = rolls.filter(frame=10)
                if len(frame_rolls) == 3:
                    game.completed = True
                    game.save()
                    return game_completed_response
                break  # Stay in the 10th frame
            i += 1  # Move to the next roll

        # Handle frame-specific logic based on frame count
        frame_rolls = rolls.filter(frame=current_frame)

        if current_frame == 10:
            if len(frame_rolls) == 3:
                game.completed = True
                game.save()
                return game_completed_response

            if len(frame_rolls) == 1 and frame_rolls[0].knocked_down_pins == 10:
                roll_number = 2
            elif len(frame_rolls) == 2:
                first_roll = frame_rolls[0]
                second_roll = frame_rolls[1]
                if first_roll.knocked_down_pins == 10 or (
                    first_roll.knocked_down_pins + second_roll.knocked_down_pins == 10
                ):
                    roll_number = 3
                else:
                    game.completed = True
                    game.save()
                    return game_completed_response
            else:
                roll_number = 1
        else:
            if len(frame_rolls) == 0:
                roll_number = 1
            elif len(frame_rolls) == 1:
                if frame_rolls[0].knocked_down_pins + knocked_down_pins > 10:
                    return Response(
                        {
                            "error": "Total knocked down pins for the frame cannot exceed 10"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if frame_rolls[0].knocked_down_pins == 10:
                    current_frame += 1
                    roll_number = 1
                else:
                    roll_number = 2

        if roll_number is None:
            return Response(
                {"error": "Could not determine roll number"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Create the roll record
        roll = Roll.objects.create(
            game=game,
            frame=current_frame,
            roll_number=roll_number,
            knocked_down_pins=knocked_down_pins,
        )

        if (
            current_frame == 10
            and len(frame_rolls) == 2
            and sum([r.knocked_down_pins for r in frame_rolls]) < 10
        ):
            game.completed = True
            game.save()

        # Serialize and return the roll data
        serializer = RollSerializer(roll)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameScoreView(views.APIView):
    """
    API view to retrieve the score for a specific game.

    This view allows players to get the current score of their game.
    """

    def get(self, request, game_id):
        """
        Retrieve the score for a specific game.

        Parameters:
            request (Request): The HTTP request object.
            game_id (int): The ID of the game.

        Returns:
            Response: The response object containing the score or an error message.
        """
        # Retrieve the game or return an error if it doesn't exist
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Calculate the score for the game
        score = calculate_score(game=game)
        return Response({"score": score}, status=status.HTTP_200_OK)


class GameSummaryView(views.APIView):
    """
    API view to generate a game summary for a specific bowling game.
    """

    def get(self, request, game_id):
        """
        Generate a game summary for a specific game.

        Parameters:
            request (Request): The HTTP request object.
            game_id (int): The ID of the game.

        Returns:
            Response: The response object containing the game summary or an error message.
        """
        # Retrieve the game or return an error if it doesn't exist
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Generate the game summary
        summary = generate_game_summary(game)

        return Response({"summary": summary}, status=status.HTTP_200_OK)
