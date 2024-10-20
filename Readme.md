# Bowling Game API with LLM Integration 🎳
This bowling game API project allows users to create games, record rolls, get the current score, and request a natural language summary using a Large Language Model (LLM). The game follows standard bowling rules, and the LLM summarizes the game state.

## Installation and Setup
1. **Clone the Repository**
  
    ```bash
    git clone https://github.com/Unique-01/Bowling_Game_API.git
    cd Bowling_Game_API
    ```

2. **Set Up Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set up Environmental variables**  
Create a `.env` file in the project root directory with the following keys:
    ```bash
    SECRET_KEY=your-django-secret-key
    OPENAI_API_KEY=your-openai-api-key
    ```
    - `SECRET_KEY`: Django secret key for cryptography.
    - `OPENAI_API_KEY`: API key for accessing OpenAI's GPT model.
5. **Apply Migrations**
    ```bash
    python manage.py migrate
    ```
6. **Run the server**
    ```bash
    python manage.py runserver
    ```


## API Endpoints
1. **GET /games/**
   - **Description**: Retrieve a list of created games.
   - **Request Body**: None
   - **Response**:
     
     ```json
     [
        {
         "id": 1,
         "title": "Game title",
         "created_at": "2024-10-20T20:15:04.306397Z",
         "completed": false
       },
       {
         "id": 1,
         "title": "Game title",
         "created_at": "2024-10-20T20:15:04.306397Z",
         "completed": false
       }
     ]
     ```
2. **POST /games/**
   - **Description**: Create a new game
   - **Request Body (Optional)**:

     ```json
     {
       "title": "Game title"
     }
     ```
   - **Response**:

     ```json
     {
       "id": 1,
       "title": "Game title",
       "created_at": "2024-10-20T20:15:04.306397Z",
       "completed": false
     }
     ```
3. **POST /games/{game_id}/rolls/**
   - **Description**: Record a roll for a specific game.
   - **Request Body**:

     ```json
     {
       "knocked_down_pins": 5
     }
     ```
   - **Response**:

     ```json
     {
       "id": 1,
       "game": 1,
       "frame": 1,
       "roll_number": 1,
       "knocked_down_pins": 5,
       "created_at": "2024-10-20T20:24:01.984493Z"
     }
     ```
4. **GET /games/{game_id}/score/**
    - **Description**:  Get the current score of the game.
    - **Request Body**: None
    - **Response**:

      ```json
       {
         "score":5
       }
       ```
5. **GET /games/{game_id}/summary/**
    - **Description**:  Get the summary of the current game.
    - **Request Body**: None
    - **Response**:

      ```json
       {
          "summary": "In Game ID 1, there has been 1 roll so far in Frame 1, where 5 pins were knocked down. The game is currently in progress."
      }
       ```
## Testing
1. **Run Tests**: Use the Django `manage.py` command to run the test suite

   ```bash
   python manage.py test
   ```
3. **Test Cases**: The test suite covers the following cases:
   - Listing games.
   - Creating new games
   - Recording rolls
   - Handling edge cases like completed games, invalid rolls and nonexistent games.
   - Fetching scores
   - Generating natural language summaries using the LLM.
  

