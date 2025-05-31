import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests  # <-- added this

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    raise ValueError('Environment variable "BOT_TOKEN" not set.')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# === your GPT-2 API URL here ===
GPT2_API_URL = "http://localhost:5000/generate"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')

# === new /ai command ===
@bot.command(name="ai")
async def ai_command(ctx, *, prompt: str):
    """Send a prompt to the GPT-2 API and return the result."""
    try:
        response = requests.post(GPT2_API_URL, json={"prompt": prompt})
        if response.status_code == 200:
            data = response.json()
            await ctx.send(data.get("text", "I didn't get a response from the AI."))
        else:
            await ctx.send(f"API error: {response.status_code}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

bot.run(BOT_TOKEN)
