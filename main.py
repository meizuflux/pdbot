	# bot.py
import os
import discord
import random
intents = discord.Intents(messages=True, guilds=True)
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

@bot.command(name='ping', help='only for cool kids')
async def ping(ctx):
	await ctx.send(f'PONG! Oh, you wanted to know the ping. The ping is {round(bot.latency * 1000)} ms')

@bot.command(name='send', help='hi')
async def send(ctx, args):
			split = args.split(' ', maxsplit=1)
			printers = (int(split[1]))
			print(f'{printers}')
			channel = bot.get_channel(int(split[0]))
			await channel.send(str(split[1]))
			

#@bot.event
#async def on_message(message):
#	print('working')
#	if message.content == 'pong':
#		await message.channel.send('That\'s not how you supposed to play the game!')

#	await bot.process_commands(message)

	

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

@bot.command(name='say', help='Says something than deletes the message')
async def say(ctx, message=None):
	await ctx.send(message)
	await ctx.message.delete()

#@bot.command(name='dm', help='Sends a direct message to a user')
#async def dm(ctx, args, message):
#	sender = ctx.author 
#	string = args
#	split = string.split(' ', maxsplit=1)
#	user = bot.get_user(int(split[0]))
#	await user.send(str(split[1]))
#	message1 = (str(split[1]))
#	user1 = (int(split[0]))
#	print(f'{sender} sent "{message1}" to {+user1}')

@bot.command()
async def pm(ctx: commands.Context, target: discord.User, *, message: str) -> None:
  await target.send(message)

@bot.command(name='purge', help='Purges a set amount of messages.')
async def purge(ctx, *, args):
	await ctx.message.channel.purge(limit=1+int(args))
	await ctx.channel.send(f'Deleted {args} message(s)', delete_after=3)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.event
async def on_command(context):
	channel = bot.get_channel(788471476927332382)
	user = context.author
	channelID = context.channel
	await channel.send(f'<@{user.id}> used !{context.command} in <#{channelID.id}> in {context.guild}')
	

@bot.event
async def on_message(message):
	if message.content == 'pong':
		await message.channel.send('That\'s not how you supposed to play the game!')
	if not message.guild:
		channel = bot.get_channel(788471476927332382)
		user = message.author
		creationtime = message.created_at
		embed = discord.Embed(title='*INCOMEING MESSAGE*', description=f'<@{user.id}> sent "{message.content}"')
		embed.colour = 0xFFFFFF
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.set_footer(text=f"Sent at {creationtime}") 
	if not message.guild:
			sender = message.author 
			string = message.content
			split = string.split(' ', maxsplit=1)
			channel = bot.get_channel(int(split[0]))
			await channel.send(str(split[1]))
			message1 = (str(split[1]))
			channelid1 = (int(split[0]))
			print(f'{sender} sent "{message1}" to {+channelid1}')

	await bot.process_commands(message)

@bot.event
async def on_command(ctx):
	channel = bot.get_channel(788471476927332382)
	user = ctx.author
	channelID = ctx.channel
	creationtime = ctx.message.created_at
	embed = discord.Embed(title='Command Use', description=f'<@{user.id}> used `!{ctx.command}` in <#{channelID.id}> in {ctx.guild}')
	embed.colour = 0xFFFFFF
	embed.set_thumbnail(url=ctx.author.avatar_url)
	embed.set_footer(text=f"Sent at {creationtime}")  

	await channel.send(embed=embed)


keep_alive()
bot.run(token)