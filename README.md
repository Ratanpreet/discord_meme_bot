Discord AI Meme Bot

A powerful and funny Discord bot that automatically generates context-aware memes based on user prompts. 

Instead of just slapping text onto a random image, this bot uses AI Sentence Transformers to find the most relevant meme template for your prompt, and then uses a local LLaVA Vision-Language Model (via Ollama) to generate a witty, sarcastic, and funny caption that fits both your prompt and the meme template. Finally, it dynamically renders the text onto the image and sends it directly to your Discord channel.

Features

- Smart Template Selection: Uses sentence-transformers to match your text prompt against a library of meme templates and their tags/descriptions.
- AI Meme Captions: Uses Ollama running the llava model to write highly shareable, humorous, and ironic captions without being overly literal.
- Dynamic Image Generation: Uses Pillow (PIL) to accurately wrap and render text with standard meme formatting (white text with a black outline) onto the templates.
- Easy Discord Integration: Simple slash command (/meme) to instantly generate and post memes to your discord server.

Prerequisites

Before running this bot, you must have the following installed on your machine:
1. Python 3.8+
2. Ollama: You need Ollama running locally. Download it from ollama.com.
3. LLaVA Model in Ollama: Pull the llava model by running this command in your terminal:
   ollama run llava:7b
4. A Discord Bot Token: You need to create a bot on the Discord Developer Portal and grab its token. Remember to enable "Message Content Intent" in the bot settings.

Installation

1. Clone or Download the Repository
2. Install Python Dependencies
   It's recommended to use a virtual environment. Install the required packages:
   pip install discord.py python-dotenv sentence-transformers transformers torch pillow requests
3. Set Up Meme Templates
   Ensure you have your templates directory filled with meme template images, and a templates.json file configuring their metadata (ids, descriptions, tags, and text positions).

Configuration

Create a .env file in the root directory of the project (if it doesn't already exist) and add your Discord Bot Token:

DISCORD_BOT_TOKEN=your_discord_bot_token_here

How to Run

1. Make sure Ollama is running in the background.
2. Start the Discord bot by running:
   python discord_bot.py
3. The console will display "Bot connected as <YourBotName>" when it's ready.

Usage

Once the bot is in your Discord server, you can interact with it using the following commands:

- /meme <your prompt>: Generates a custom meme. 
  - Example: /meme when the code compiles on the first try but you don't know why
- /shutdown: Gracefully disconnects the bot and turns it off (Restricted to the bot owner).

How It Works Under the Hood

1. User requests a meme: The user types /meme <prompt> in Discord.
2. Template Matching (memebot_main.py): The bot encodes the user's prompt using the all-MiniLM-L6-v2 sentence transformer, and compares the cosine similarity against embedded descriptions of all templates in templates.json. It picks the best matching image.
3. AI Captioning: A context prompt, containing the user's idea and the selected template's description, is sent to the local LLaVA model via the Ollama API (http://localhost:11434/api/chat). The AI crafts a funny caption.
4. Rendering: Pillow reads the template image and the AI's caption, formats the text, draws a black outline and white fill, and saves it as output_meme.jpg.
5. Delivery: The bot uploads the final output_meme.jpg to the Discord channel.

Troubleshooting

- Bot not responding to commands: Ensure you enabled the Message Content Intent in the Discord Developer Portal under the Bot tab.
- Connection Refused Error: The bot uses http://localhost:11434 to communicate with the AI. Make sure Ollama is open and running.
- Font Errors: The bot tries to use arialbd.ttf (Windows Arial Bold). If you are on Linux or macOS, you might need to change the font path in memebot_main.py to a valid TrueType font on your system.
