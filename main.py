import os
import discord
import json
import aiohttp
import asyncdagpi
from discord.ext import commands
#from pretty_help import PrettyHelp
from keep_alive import keep_alive
from help.help import MyNewHelp
import datetime
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MongoDB'])

db = client.prefixes

dagpikey = os.environ['dagpikey']

async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("c//")(bot, message)

    try:
        data = await db.pre.find_one({"_id": message.guild.id})
        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            await db.pre.insert_one({"_id": message.guild.id, "prefix": "c//"})
            return commands.when_mentioned_or("c//")(bot, message)
        return commands.when_mentioned_or(data['prefix'])(bot, message)
    except:
        return commands.when_mentioned_or("c//")(bot, message)


activity = discord.Activity(type=discord.ActivityType.listening,
                            name='c//help')
bot = commands.Bot(command_prefix=get_prefix,
                   case_insensitive=True,
                   activity=activity,
                   intents=discord.Intents(guilds=True,
                                           members=True,
                                           messages=True,
                                           reactions=True,
                                           presences=True))
#bot.help_command = PrettyHelp(active_time=30, color=discord.Colour.blue(), index_name='Cute Bot', sort_commands=False, show_index=True)
bot.author_id = 777893499471265802
bot.dagpi = asyncdagpi.Client(dagpikey)
bot.session = aiohttp.ClientSession()
bot.embed_color = 0x9c5cb4  #0x1E90FF
bot.help_command = MyNewHelp(command_attrs=dict(hidden=True))
bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MongoDB'])
bot.data = bot.mongo.data

bot.description = '```py\n  ____      _       \n / ___|   _| |_ ___ \n| |  | | | | __/ _ \n| |__| |_| | ||  __/\n \____\__,_|\__\___|```'


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    bot.start_time = datetime.datetime.utcnow()


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
    'cogs.misc', 'cogs.fun', 'cogs.tenor', 'cogs.devcommands', 'cogs.tracking',
    'cogs.speak', 'cogs.api', 'cogs.errorhandler', 'cogs.owner',
    'cogs.prefixes', 'jishaku', 'cogs.beatsaber', 'cogs.imagemanip',
    'cogs.invites', 'cogs.mongo', 'cogs.zane', 'cogs.eco'
]

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

keep_alive()
bot.run(os.environ['DTOKEN'])
