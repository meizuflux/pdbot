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
async def send(ctx, channel: discord.TextChannel, *, message):
	await channel.send(message) 
	await ctx.message.delete()

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

@bot.command()
async def pm(ctx: commands.Context, target: discord.User, *, message: str) -> None:
  await target.send(message)

@bot.command(name='purge', help='Purges a set amount of messages.')
async def purge(ctx, *, args):
	await ctx.message.channel.purge(limit=1+int(args))
	await ctx.channel.send(f'Deleted {args} message(s)', delete_after=3)

@bot.command(name='pp', help='cock')
async def cock(ctx, args):
	args = args.capitalize()
	if args == 'I' or 'You':
		await ctx.send(f'{args} have a small pp')
	else:
		await ctx.send(f'{args} has a small pp')


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
		if message.author.id == bot.user.id:
			return
		else:
			channel = bot.get_channel(788471476927332382)
			creationtime = message.created_at
			embed = discord.Embed(title='*INCOMEING MESSAGE*', description=f'{message.author} sent "{message.content}"')
			embed.colour = 0xFFFFFF
			embed.set_thumbnail(url=message.author.avatar_url)
			embed.set_footer(text=f"Sent at {creationtime}")
			await channel.send(embed=embed)
			return
	if message.channel.id == int(789329010080743444):
		await message.add_reaction('\N{UPWARDS BLACK ARROW}')
		await message.add_reaction('\N{DOWNWARDS BLACK ARROW}')

	await bot.process_commands(message)

@bot.event
async def on_command(ctx):
	channel = bot.get_channel(788471476927332382)
	channelID = ctx.channel
	creationtime = ctx.message.created_at
	embed = discord.Embed(title='Command Use', description=f'{ctx.author} used `!{ctx.command}` in #{channelID.name} in {ctx.guild}')
	embed.colour = 0xFFFFFF
	embed.set_thumbnail(url=ctx.author.avatar_url)
	embed.set_footer(text=f"Sent at {creationtime}")  

	await channel.send(embed=embed)


keep_alive()
bot.run(token)