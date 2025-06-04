# -- Standard library imports -- #
import os
import json

# -- discord.py -- #
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# -- included librarys -- #
import markov_babbler as Babbler

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    raise ValueError('Environment variable "BOT_TOKEN" not set.')

# -- Data storage for markov commands -- #
messages_sent = 0
need_new_stats = True
stats = {}

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
    global stats
    await interaction.response.send_message(Babbler.babble(stats, sentences))

# -- random command -- #
@bot.tree.command(name="anagram", description="Figure out if two words are anagrams")
@app_commands.describe(word1="first word", word2="Second word")
async def anagram(interaction: discord.Interaction, word1: str, word2: str):
    angrm = "are" if sorted(word1.lower().strip()) == sorted(word2.lower().strip()) else "are not"
    await interaction.response.send_message(f"{word1} and {word2} {angrm} anagrams.")
 
@bot.event
async def on_message(message):
    global messages_sent
    if message.author.bot:
        return
    if not (message.content and not message.embeds and not message.attachments):
        return

    messages_sent += 1
    if need_new_stats:
        stats = Babbler.get_cloud_stats()
    stats = Babbler.get_stats(message.content, stats)
    if messages_sent >= 15:
        Babbler.save_cloud_stats(stats)
        need_new_stats = True

bot.run(BOT_TOKEN)