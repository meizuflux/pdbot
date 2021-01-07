from discord.ext import commands
import discord
import random

class Misc(commands.Cog):
	"""For commands that don't really have a category"""
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(name='guilds', help='list of guilds')
	async def guilds(self, ctx):
		for guild in self.bot.guilds:
			await ctx.send(guild)

	@commands.command(name='pfp', help='just use it 4Head')
	async def pfp(self, ctx, *, member: discord.Member=None):
			await ctx.send(member.avatar_url)
	
	@commands.command(name='puppy', help='A cute little puppy doing cute things')
	async def puppy(self, ctx):
		await ctx.author.send('https://www.youtube.com/watch?v=j5a0jTc9S10&list=PL3KnTfyhrIlcudeMemKd6rZFGDWyK23vx&index=11')
		await ctx.send('Video sent successfully')

	@commands.command(name='ping', help='only for cool kids')
	async def ping(self, ctx):
		await ctx.send(f'PONG! Oh, you wanted to know the ping. The ping is {round(self.bot.latency * 1000)} ms')
		
	@commands.command(name='source', help='Bots source code')
	async def source(self, ctx):
		embed=discord.Embed(description='https://github.com/ppotatoo/pdbot')
		await ctx.send(embed=embed)
		
	@commands.command(name='creator', help='use it')
	async def creator(self, ctx):
		thelist = ['<:sad:790608581615288320>', '<:DogKek:790932497856725013>', '<:4Head:790667956963115068>', '<:Sadge:789590510225457152>']
		if ctx.author.id == int(777893499471265802):
			await ctx.send('you <:PogYou:791007602741739610>')
		else:
			await ctx.send(f'not you {random.choice(thelist)}')

	
	@commands.command(name='purge')
	@commands.has_permissions(manage_messages=True) # can also do manage_guild, your choice.
	async def purge(ctx, *, args):
		await ctx.message.channel.purge(limit=1+int(args))
		await ctx.channel.send(f'Deleted {args} message(s)', delete_after=2)


	@commands.command(name='activity', aliases=['a'])
	@commands.is_owner()
	async def presence(self, ctx, atype: str, *, activity=None):
		atype = atype.lower()
		if atype == 'default':
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'@{self.bot.user.name}'))
		if atype == 'watching':
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
		if atype == 'listening':
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
		if atype == 'playing':
			await self.bot.change_presence(activity=discord.Game(name=activity))
		if atype == 'streaming':
			await self.bot.change_presence(activity=discord.Streaming(name=activity, url='https://twitch.tv/ppotatoo_'))
		if atype == 'competing':
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=activity))

	

def setup(bot):
	bot.add_cog(Misc(bot))