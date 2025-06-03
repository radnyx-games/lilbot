# -- Standard library imports -- #
import os
import json

# -- discord.py -- #
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# -- IDK it's for the markov babbler commands -- #
import markov_babbler as Babbler
import dropbox

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    raise ValueError('Environment variable "BOT_TOKEN" not set.')

# -- Data storage for markov commands -- #
DROPBOX_KEY = os.getenv('DROPBOX_KEY')
if DROPBOX_KEY is None:
    raise ValueError('Environment variable "DROPBOX_KEY" not set.')
dbx = dropbox.Dropbox(DROPBOX_KEY)
messages_sent = 0
need_new_stats = True

def get_cloud_stats():
    try:
        metadata, res = dbx.files_download("/lilguys-markov/stats.json")
        data = res.content
        
        stats = json.loads(data.decode('utf-8'))
        need_new_stats = False
        return stats
    except Exception as e:
        need_new_stats = False
        return {}

def save_cloud_stats(stats):
    stats_str = json.dumps(stats)
    stats_bytes = stats_str.encode('utf-8')
    dbx.files_upload(stats_bytes, '/lilguys-markov/stats.json', mode=dropbox.files.WriteMode.overwrite)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')

# -- Markov commands -- #
@bot.tree.command(name="babble", description="Generate Markov babble")
@app_commands.describe(sentences="Number of sentences to generate")
async def babble(interaction: discord.Interaction, sentences: int):
    stats = get_cloud_stats()
    await interaction.response.send_message(Babbler.babble(stats, sentences))

@bot.event
async def on_message(message):
    global messages_sent
    if message.author.bot:
        return
    if not (message.content and not message.embeds and not message.attachments):
        return

    messages_sent += 1
    if need_new_stats:
        stats = get_cloud_stats()
    stats = Babbler.get_stats(message.content, stats)
    if messages_sent >= 15:
        save_cloud_stats(stats)
        need_new_stats = True

bot.run(BOT_TOKEN)