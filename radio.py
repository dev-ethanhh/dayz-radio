# Libraries
import discord
import random
import csv
from datetime import datetime

''' PARAMETERS ''' 
# Discord bot token
var_bot_token = ""

# Discord server ID
var_bot_server = 0

# Discord channel ID (Warning: the bot will delete previous messages in this channel)
var_bot_channel = 0

# Discord channel used to log radio messages
var_log_channel = 0

# Crackling frequency (0 to 10)
var_gresillement = 3

# Crackling sounds
liste_gresillement = ["shkkkk", "ksssss", "zzzzz"]

# Jump frequenty (0 to 10)
var_jump = 3

# CSV log file for original (unmodified) messages
var_log_csv = 'data/logs.csv'

# CSV log file for modified messages
var_messages_csv = 'data/messages.csv'

intents = discord.Intents.all()
client = discord.Client(intents=intents)

def create_log_csv(message):
    with open(var_log_csv, mode='a', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message.author.name, message.content])

def save_modified_message(modified_message, message):
    with open(var_messages_csv, mode='a', newline='') as messages_file:
        messages_writer = csv.writer(messages_file)
        messages_writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message.author.name, modified_message, 'FALSE'])

def create_log_embed(message):
    embed = discord.Embed(title=f"{message.author.name}#{message.author.discriminator} ({message.author.id})", description=f"{message.content}\nSent on {message.created_at}")
    return embed

def add_gresillement_and_jump(phrase, var_gresillement, var_jump, liste_gresillement):
    phrase_modifiee = ""
    for char in phrase:
        if random.uniform(0, 100) < var_gresillement:
            char = char + random.choice(liste_gresillement)
        if random.uniform(0, 100) < var_jump:
            char = "\_"
        phrase_modifiee += char
    return phrase_modifiee

@client.event
async def on_ready():
    channel = client.get_channel(var_bot_channel)
    await channel.purge()
    with open(var_messages_csv, mode='w', newline='') as messages_file:
        messages_file.seek(0)
        messages_file.truncate()


@client.event
async def on_message(message):
    try:
        if message.guild.id == var_bot_server and message.channel.id == var_bot_channel and message.author != client.user:
            await message.delete()
            modified_message = add_gresillement_and_jump(message.content, var_gresillement, var_jump, liste_gresillement)
            embed = discord.Embed(title="Radio Message", description=modified_message)
            await message.channel.send(embed=embed)
            await client.get_channel(var_log_channel).send(embed=create_log_embed(message))
            create_log_csv(message)
            save_modified_message(modified_message, message)
    except:
        if message.author != client.user and isinstance(message.channel, discord.DMChannel):
            if message.author in client.get_guild(var_bot_server).members:
                modified_message = add_gresillement_and_jump(message.content, var_gresillement, var_jump, liste_gresillement)
                embed = discord.Embed(title="Radio Message", description=modified_message)
                await client.get_channel(var_bot_channel).send(embed=embed)
                await client.get_channel(var_log_channel).send(embed=create_log_embed(message))
                create_log_csv(message)
                save_modified_message(modified_message, message)

client.run(var_bot_token)
