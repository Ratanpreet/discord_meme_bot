import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Import your meme generation functions
from memebot_main import select_template, generate_caption, render_caption_on_template

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Needed to read user messages

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.command(name='meme')
async def meme(ctx, *, prompt: str):
    await ctx.send(f' Generating meme for: **{prompt}** ...')
    try:
        img_path, tmpl = select_template(prompt)
        caption = generate_caption(img_path, prompt, tmpl)
        output_path = render_caption_on_template(img_path, caption, tmpl)
        with open(output_path, 'rb') as f:
            await ctx.send(file=discord.File(f, filename='meme.jpg'))
    except Exception as e:
        await ctx.send(f'Error generating meme: {e}')
from discord.ext import commands

@bot.command(name='shutdown')
@commands.is_owner()  # Only you (the bot owner) can use this command
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.close()  # Gracefully disconnects the bot

if __name__ == '__main__':
    bot.run(TOKEN)
