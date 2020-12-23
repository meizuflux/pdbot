	# bot.py
import os
import discord
import random
import json
intents = discord.Intents(messages=True, guilds=True)
from discord.ext import commands
from pretty_help import PrettyHelp 	


bot = commands.Bot(command_prefix="!", help_command=PrettyHelp(), case_insensitive=True)
bot.author_id = 777893499471265802

token = os.environ['DTOKEN']

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='createchannel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)





@bot.command()
async def pm(ctx: commands.Context, target: discord.User, *, message: str) -> None:
  await target.send(message)

@bot.command(name='purge', help='Purges a set amount of messages.')
async def purge(ctx, *, args):
	if args == 'all':
		await ctx.message.channel.purge(limit=10000000000000000)
		await ctx.channel.send(f'Deleted {args} messages', delete_after=3)
	else: 
		await ctx.message.channel.purge(limit=1+int(args))
		await ctx.channel.send(f'Deleted {args} message(s)', delete_after=3)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
	

#@bot.event
#async def on_message(message):
	#if bot.user in message.mentions:
	#	await message.channel.send(f'<@{message.author.id}>, my prefix on this server is `!`')
#	if message.content == 'pong':
#		await message.channel.send('That\'s not how you supposed to play the game!')
	#if message.content == 'patience':
	#    patienceembed = discord.Embed(description='patoence')
	 #   await message.channel.send(embed=patienceembed)

	#await bot.process_commands(message)



extensions = [
	'cogs.misc',
	'cogs.examplecog',
	'cogs.fun',
	'cogs.tenor',
	'cogs.devcommands',
	'cogs.logging',
	'cogs.reactions',
	'cogs.speak',
	'cogs.testingjson'
]

if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)
	
bot.run(token)