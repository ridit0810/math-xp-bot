# 🤖 Discord Math & Utility Bot

A feature-rich Discord bot that combines educational math games with server utility and moderation tools.

## ✨ Features

-   **🧠 Math Game**: Interactive quizzes for 11th & 12th grade topics (e.g., Geometric Progression).
    -   Select Grade -> Topic -> Difficulty.
    -   Earn XP and level up by answering correctly!
-   **🏆 XP System**: Track user progress and levels.
-   **🛠️ Utility**:
    -   `ping`: Check bot latency.
    -   `avatar`: View user avatars.
    -   `serverinfo` / `userinfo`: Get detailed stats.
-   **🛡️ Moderation**:
    -   `clear`: Bulk delete messages.
-   **🎉 Fun**:
    -   `poll`: Create interactive polls.
    -   `roll`: Roll a dice.
-   **⏰ Reminders**: Set custom reminders (e.g., "10m", "1h").

## 📦 Installation

1.  **Install Python**: Ensure you have Python 3.8+ installed.
2.  **Clone/Download**: Download this project folder.
3.  **Install Dependencies**:
    Open your terminal/command prompt in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  Create a file named `.env` in the main folder.
2.  Add your Discord Bot Token inside it:
    ```env
    DISCORD_TOKEN=your_token_here
    ```

## 🚀 How to Run

Run the following command in your terminal:

```bash
python main.py
```

## 📜 Basic Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| **`.help`** | Shows the list of all commands. | `.help` |
| **`.math`** | Starts the interactive Math Game. | `.math` |
| **`.ping`** | Checks the bot's response time. | `.ping` |
| **`.poll <msg>`** | Creates a poll with 👍/👎. | `.poll Is this cool?` |
| **`.remindme <time> <msg>`** | Sets a reminder. | `.remindme 10m Take a break` |
| **`.clear <amount>`** | Deletes messages (Admin only). | `.clear 5` |
