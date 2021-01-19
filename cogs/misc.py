from discord.ext import commands
import discord
import random
import inspect
import os

class Misc(commands.Cog):
	"""For commands that don't really have a category"""
	def __init__(self, bot):
		self.bot = bot

	def mng_msg():
		def predicate(ctx):
			if ctx.author.id == 777893499471265802:
				return True
			if ctx.author.guild_permissions.manage_messages == True:
				return True
			else: 
				return False
		return commands.check(predicate)
		
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
		
		
	@commands.command(name='creator', help='use it')
	async def creator(self, ctx):
		thelist = ['<:sad:790608581615288320>', '<:DogKek:790932497856725013>', '<:4Head:790667956963115068>', '<:Sadge:789590510225457152>']
		if ctx.author.id == int(777893499471265802):
			await ctx.send('you <:PogYou:791007602741739610>')
		else:
			await ctx.send(f'not you {random.choice(thelist)}')

	
	@commands.command(name='purge')
	@mng_msg() # can also do manage_guild, your choice.
	async def purge(self, ctx, amount: int):
		await ctx.channel.purge(limit=1+int(amount))
		await ctx.send(f'Deleted {amount} message(s)', delete_after=2)


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
	
	@commands.command(name='whois')
	async def who(self, ctx, member: discord.Member):
		mention_roles = [i.mention for i in member.roles[1:]]
		join = member.joined_at.strftime("%m/%d/%Y")
		create = member.created_at.strftime("%m/%d/%Y")
		embed=discord.Embed(title=str(member), description=f'**Joined:** {join}\n**Account Creation:** {create}')
		embed.set_thumbnail(url=member.avatar_url)
		embed.add_field(name='Roles', value=', '.join(mention_roles))
		if member.name != member.display_name:
			embed.set_footer(text=f'{member.id} • {member.display_name}')
		else:
			embed.set_footer(text=member.id)
		await ctx.send(embed=embed)

	@commands.command(name='serverinfo', usage='', help='Shows info about the server')
	async def info(self, ctx):
		guild = ctx.guild
		roles = [role.name.replace('@', '@\u200b') for role in guild.roles]
		e = discord.Embed()
		e.title = guild.name
		e.description = f'**ID:** {guild.id}'
		e.set_thumbnail(url=ctx.guild.icon_url)
		fmt = f'Total: {guild.member_count}'
		e.add_field(name='Members', value=fmt, inline=False)
		e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles')
		e.set_footer(text='Created').timestamp = guild.created_at
		await ctx.send(embed=e)

	@commands.command()
	async def source(self, ctx, *, command: str = None):
		source_url = 'https://github.com/ppotatoo/pdbot'
		branch = 'master'
		if command is None:
			return await ctx.send(source_url)
		if command == 'help':
			e=discord.Embed(description='https://pypi.org/project/discord-pretty-help/')
			await ctx.send(embed=e)			
		elif command.startswith('jsk') or command.startswith('jishaku'):
			e=discord.Embed(description='https://pypi.org/project/jishaku/')
			await ctx.send(embed=e)
		else:
			obj = self.bot.get_command(command.replace('.', ' '))
			if obj is None:
				return await ctx.send('Could not find command.')
			src = obj.callback.__code__
			module = obj.callback.__module__
			filename = src.co_filename
		
			lines, firstlineno = inspect.getsourcelines(src)
			if not module.startswith('discord'):
				location = os.path.relpath(filename).replace('\\', '/')
			else:
				location = module.replace('.', '/')
				source_url = 'https://github.com/ppotatoo/pdbot'
				branch = 'master'

			final_url = f'<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>'
			e=discord.Embed(description=final_url)
			await ctx.send(embed=e)


def setup(bot):
	bot.add_cog(Misc(bot))