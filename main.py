	# bot.py
import os
import discord
import json
intents = discord.Intents(messages=True, guilds=True)
from discord.ext import commands
from pretty_help import PrettyHelp 	
from keep_alive import keep_alive

async def pre(bot, message):
	with open("data.json", "r") as f:
		data = json.load(f)
	return data['prefix']

bot = commands.Bot(command_prefix=pre, help_command=PrettyHelp(),case_insensitive=True)
bot.author_id = 777893499471265802

token = os.environ['DTOKEN']

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

blist = []

@bot.check
async def blacklist(ctx):
	if ctx.author.id in blist:
		return False
	else: 
		return True

extensions = [
	'cogs.misc',
	'cogs.fun',
	'cogs.tenor',
	'cogs.devcommands',
	'cogs.tracking',
	'cogs.reactions',
	'cogs.speak',
	'cogs.testingjson',
	'cogs.api',
	'cogs.errorhandler',
	'cogs.admin'
]

if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)

keep_alive()
bot.run(token)
