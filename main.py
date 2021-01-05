	# bot.py
import os
import discord
import random
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


@bot.command(name='createchannel', hidden=True)
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

blist = []

@bot.check
async def blacklist(ctx):
	if ctx.author.id in blist:
		return False
	else: 
		return True

@bot.command(name='block', hidden=True)
@commands.has_permissions(manage_channels=True)
async def block(ctx, *, member: discord.Member=None):
	blist.append(int(member.id))
	await ctx.send(f'Added {member} to the blacklist.')






@bot.command(hidden=True)
@commands.is_owner()
async def pm(ctx: commands.Context, target: discord.User, *, message: str) -> None:
  await target.send(message)

@bot.command(name='purge', help='Purges a set amount of messages.', hidden=True)

@commands.has_permissions(manage_messages=True) # can also do manage_guild, your choice.
async def purge(ctx, *, args):
	if args == 'all':
		await ctx.message.channel.purge(limit=10000000000000000)
		await ctx.channel.send(f'Deleted {args} messages', delete_after=3)
	else: 
		await ctx.message.channel.purge(limit=1+int(args))
		await ctx.channel.send(f'Deleted {args} message(s)', delete_after=3)





extensions = [
	'cogs.misc',
	'cogs.examplecog',
	'cogs.fun',
	'cogs.tenor',
	'cogs.devcommands',
	'cogs.tracking',
	'cogs.reactions',
	'cogs.speak',
	'cogs.testingjson',
	'cogs.api',
	'cogs.errorhandler'
]

if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)

keep_alive()
bot.run(token)
