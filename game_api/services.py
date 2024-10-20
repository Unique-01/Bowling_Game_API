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


from openai import OpenAI
from decouple import config


def generate_game_summary(game):
    """
    Generates a summary of a bowling game using OpenAI's API.

    Args:
        game (Game): The Game instance for which to generate the summary.

    Returns:
        str: A summary of the bowling game, including total rolls and pin counts for each roll.
    """
    client = OpenAI(api_key=config("OPENAI_API_KEY"))

    # Retrieve all rolls for the game, ordered by creation time
    rolls = game.rolls.all().order_by("created_at")

    # Prepare the prompt for the OpenAI API
    prompt = (
        f"Summarize a bowling game with the following stats:\n"
        f"Game ID: {game.id}\n"
        f"Total Rolls: {len(rolls)}\n"
    )

    # Add details of each roll to the prompt
    for roll in rolls:
        prompt += f"Frame {roll.frame}, Roll {roll.roll_number}: {roll.knocked_down_pins} pins knocked down.\n"

    # Indicate if the game is completed or still in progress
    prompt += "Game Completed" if game.completed else "Game In Progress"

    # Call the OpenAI API to generate the summary
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the model to use
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,  # Set the temperature for response variability
    )

    # Return the generated summary content
    return response.choices[0].message.content
