from discord.ext import commands
import discord

class Misc(commands.Cog):
	"""For commands that don't really have a category"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='pfp', help='just use it 4Head')
	async def pfp(self, ctx):
			await ctx.send(ctx.message.author.avatar_url)
	
	@commands.command(name='puppy', help='A cute little puppy doing cute things')
	async def puppy(self, ctx):
		await ctx.author.send('https://www.youtube.com/watch?v=j5a0jTc9S10&list=PL3KnTfyhrIlcudeMemKd6rZFGDWyK23vx&index=11')
		await ctx.send('Video sent successfully')

	@commands.command(name='ping', help='only for cool kids')
	async def ping(self, ctx):
		await ctx.send(f'PONG! Oh, you wanted to know the ping. The ping is {round(self.bot.latency * 1000)} ms')

def setup(bot):
	bot.add_cog(Misc(bot))