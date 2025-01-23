# WellBot - Create Your Personalized Chatbot for Wellbeing

This project allows users to create their own customizable AI chatbot with tailored personalities, tones, and communication styles to improve personal wellbeing. Users can input profiles for both the chatbot and themselves through JSON files or interactive input. The chatbot can also be fine-tuned using pre-prompted instructions.

---

## Features

- **Custom User Profiles**: Define the user's details like name, nickname, age, and gender.
- **Custom Chatbot Profiles**: Create detailed profiles for the chatbot, including its role, tone, slang preferences, language, and personality.
- **Pre-Prompted Bots**: Use a folder containing `system.txt` and `tone.txt` for a preconfigured bot personality.
- **Export Sessions**: Save chatbot profiles, user profiles, and conversations in a structured format for later use.

---

## How to Run

To run the project, use the following command:

```bash
python main.py --user <input_type> [--user_profile <path_to_user_json>] --bot <bot_type> [--bot_profile <path_to_bot_json> | --module <module_folder>] [--export]
```

### Arguments

---

#### User Options:

- `--user`: Specifies the input type for the user.
  - **Options**:
    - `json`: Provide user details via a JSON file. Requires the `--user_profile` argument.
    - `input`: Manually input user details during runtime.
  - **Example**:
    ```bash
    --user json --user_profile modules/user/user-1.json
    ```

- `--user_profile`: Path to a JSON file containing user details (required if `--user` is `json`).
  - **Example user JSON file**:
    ```json
    {
      "full_name": "Winar Marco",
      "nickname": "Mar",
      "age": "21",
      "gender": "Male"
    }
    ```

#### Bot Options:

- `--bot`: Specifies the input type for the bot.
  - **Options**:
    - `input`: Manually input bot details during runtime.
    - `json`: Provide bot details via a JSON file. Requires the `--bot_profile` argument.
    - `preprompt`: Use pre-prompted instructions from a folder. Requires the `--module` argument.
  - **Example**:
    ```bash
    --bot json --bot_profile modules/bot/bot-1.json
    ```

- `--bot_profile`: Path to a JSON file containing bot details (required if `--bot` is `json`).
  - **Example bot JSON file**:
    ```json
    {
      "name": "Andrew",
      "role": "Teman",
      "description": "",
      "gender": "Male",
      "communication_style": "",
      "nickname": "bro",
      "language": "Indonesia",
      "personality": "Baik, Bijak"
    }
    ```

- `--module`: Path to a folder containing `system.txt` and `tone.txt` (required if `--bot` is `preprompt`).
  - **Example `system.txt`**:
    ```
    ### System Prompt for Mental Health Chatbot

    **Goal**:
    To be an active listener, showing empathy and encouragement. Provide light, actionable, and easy-to-follow advice.

    **Example Conversation**:
    User: Halo.
    Bot: Halo! Ada yang mau dibicarakan? 😊
    ```

  - **Example `tone.txt`**:
    ```
    ### Tone Adjustment
    1. Use a casual tone.
    2. Include slang like "Gue", "Bro", "Mantap".
    3. Add emojis to keep the vibe light.
    ```

#### Export Option:
- `--export`: A flag to export the session details, including user profile, bot profile, and conversation history, into a folder named `chat_<timestamp>`.

---

## Example Command

Here’s a complete example command:

```bash
python main.py --user json --user_profile modules/user/user-1.json --bot json --bot_profile modules/bot/bot-1.json --export
```
#### Explanation:
- `--user` json: Load user details from a JSON file.
- `--user_profile`: Path to the user JSON file.
- `--bot` json: Load bot details from a JSON file.
- `--bot_profile`: Path to the bot JSON file.
- `--export`: Save the session data into an export folder.

---

## Exported Files

When `--export` is used, the following files will be generated in the `chat_<timestamp>` folder:

### 1. `user.json`: Contains user details.
   - **Example**:
     ```json
     {
       "full_name": "Winar Marco",
       "nickname": "Mar",
       "age": "21",
       "gender": "Male"
     }
     ```

### 2. `bot.json`: Contains bot details and prompts.
   - **Example**:
     ```json
     {
       "type": "json",
       "profile": {
         "name": "Andrew",
         "role": "Teman",
         "description": "",
         "gender": "Male",
         "communication_style": "",
         "nickname": "bro",
         "language": "Indonesia",
         "personality": "Baik, Bijak"
       },
       "prompt": {
         "system_prompt": "To be an active listener...",
         "tone_prompt": "Use casual tone..."
       }
     }
     ```

### 3. `conversation.json`: Contains the chat session history.
   - **Example**:
     ```json
     {
       "conversations": [
         {
           "role": "user",
           "content": "Halo."
         },
         {
           "role": "assistant",
           "content": "Halo Mar! Ada yang mau dibicarakan?"
         }
       ],
       "holistic_wellness_category": [
          "Financial",
          "Emotional",
          "Occupational"
       ]
     }
     ```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/chatbot-ai.git
   cd chatbot-ai
   ```
2. Install the dependencies:
   ```bash
   pip install requirements.txt
   ```

3. Create .env file
   ```bash
   MISTRAL_API_KEY=your_api_key
   ```

---

## Requirements

- Python 3.8+
- Required libraries (install via `pip install -r requirements.txt`):
  - `mistralai`
  - `python-dotenv`
  - `termcolor`

---

## Technology Used

- **[Mistral AI](https://mistral.ai/):** Utilized for advanced language modeling and chatbot responses, enabling the creation of personalized and empathetic conversational agents.
- **Python 3.8+:** The core programming language for building and running the application.
- **Libraries:**
  - `mistralai`: For integrating with the Mistral AI API.
  - `python-dotenv`: For securely managing environment variables.
  - `termcolor`: For enhancing terminal output with color-coded user and bot interactions.

---

## Contributing

Feel free to contribute by submitting issues or pull requests. Contributions are welcome to improve features, add more customization, or fix bugs.

---

## License

This project is licensed under the MIT License.

---

## Notes

For questions, feedback, or support, feel free to open an issue or contact the repository maintainer.

Happy chatting! 😊

