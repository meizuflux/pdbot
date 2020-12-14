	# bot.py
import os
import discord
import random
from discord.ext import commands
#from dotenv import load_dotenv


token = os.environ['DTOKEN']

#load_dotenv()
#TOKEN = os.getenv('TOKEN')
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='!')

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

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='say', help='Says something than deleted the message')
async def say(ctx, message=None):
	await ctx.send(message)
	await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.event
async def on_command(context):
	print(f'{context.author} used !{context.command} in #{context.channel} in {context.guild}')

@bot.event
async def on_message(message):
	if message.guild == False: 
		string = message.content
		split = string.split(' ')
		channel = bot.get_channel(int(split[0]))
		await channel.send(int(split[1]))





keep_alive()
bot.run(token)