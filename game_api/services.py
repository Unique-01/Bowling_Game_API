from openai import OpenAI
from decouple import config


def calculate_score(game):
    """
    Calculate the total score for a bowling game.

    Parameters:
        game (Game): The Game instance containing the rolls.

    Returns:
        int: The total score for the game.
    """
    score = 0
    rolls = list(game.rolls.all().order_by("frame", "roll_number"))
    frame_index = 0

    for frame in range(10):
        if frame_index >= len(rolls):
            break

        if rolls[frame_index].knocked_down_pins == 10:
            score += 10 + next_two_rolls(rolls, frame_index)
            frame_index += 1
        elif (
            sum([r.knocked_down_pins for r in rolls[frame_index : frame_index + 2]])
            == 10
        ):
            score += 10 + next_roll(rolls, frame_index + 2)
            frame_index += 2
        else:
            score += sum(
                [r.knocked_down_pins for r in rolls[frame_index : frame_index + 2]]
            )
            frame_index += 2

    return score


def next_two_rolls(rolls, index):
    """
    Sum the pins knocked down in the next two rolls.

    Parameters:
        rolls (list[Roll]): List of Roll instances.
        index (int): Current roll index.

    Returns:
        int: Total pins knocked down in the next two rolls.
    """
    total_score = 0

    for i in range(1, 3):  # Check index+1 and index+2
        if index + i < len(rolls):  # Ensure we're within bounds
            total_score += rolls[index + i].knocked_down_pins

    return total_score


def next_roll(rolls, index):
    """
    Get the pins knocked down in the next roll.

    Parameters:
        rolls (list[Roll]): List of Roll instances.
        index (int): Current roll index.

    Returns:
        int: Pins knocked down in the next roll, or 0 if none.
    """
    return rolls[index].knocked_down_pins if index < len(rolls) else 0


def generate_game_summary(game):
    client = OpenAI(api_key=config("OPENAI_API_KEY"))

    rolls = game.rolls.all().order_by("created_at")

    # prompt = "Summarize a bowling game with he following stats \n"
    # prompt += f"Game ID: {game.id}\n"
    # prompt += f"Total Rolls: {len(rolls)}\n"
    prompt = (
            f"Summarize a bowling game with the following stats:\n"
            f"Game ID: {game.id}\n"
            f"Total Rolls: {len(rolls)}\n"
        )

    for roll in rolls:
        prompt += f"Frame {roll.frame}, Roll {roll.roll_number}: {
            roll.knocked_down_pins} pins knocked down.\n"

    prompt += "Game Completed" if game.completed else "Game In Progress"

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}],temperature=0.8
    )
    return response.choices[0].message.content
