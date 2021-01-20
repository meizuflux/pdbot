import os
import discord
import json
from discord.ext import commands
from pretty_help import PrettyHelp 	
from keep_alive import keep_alive

async def pre(bot, message):
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)
	return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)

activity = discord.Activity(type=discord.ActivityType.listening, name=f'!help')
bot = commands.Bot(command_prefix=pre, case_insensitive=True, activity=activity, intents=discord.Intents(guilds=True, members=True, messages=True, reactions=True, presences=True))
bot.help_command = PrettyHelp(active_time=30, color=discord.Colour.blue(), index_name='Cute Bot', sort_commands=False, show_index=True)
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
		
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"


extensions = [
	'cogs.misc',
	'cogs.fun',
	'cogs.tenor',
	'cogs.devcommands',
	'cogs.tracking',
	'cogs.reactions',
	'cogs.speak',
	'cogs.api',
	'cogs.errorhandler',
	'cogs.owner',
	'cogs.prefixes',
	'jishaku',
	'cogs.beatsaber'
]

if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)
		
keep_alive()
bot.run(token)
