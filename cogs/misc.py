from discord.ext import commands
import discord
import random
import inspect
import os
from pkg_resources import get_distribution
import time
import humanize
import platform
import psutil

class Misc(commands.Cog):
	"""For commands that don't really have a category"""
	def __init__(self, bot):
		self.bot = bot
		self.process = psutil.Process(os.getpid())

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
		await ctx.send('https://www.youtube.com/watch?v=j5a0jTc9S10&list=PL3KnTfyhrIlcudeMemKd6rZFGDWyK23vx&index=11')

	@commands.command(name='ping', help='only for cool kids')
	async def ping(self, ctx):
		start = time.perf_counter()
		message = await ctx.send("Pinging ...")
		end = time.perf_counter()
		duration = (end - start) * 1000
		pong = discord.Embed(title='Ping', color=0x2F3136)
		pong.add_field(name='Typing Latency', value=f'```python\n{round(duration)} ms```')
		pong.add_field(name='Websocket Latency', value=f'```python\n{round(self.bot.latency * 1000)} ms```')
		await message.edit(content=None, embed=pong)
		
		
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
		await ctx.send(f'Set activity to `{activity}` with type `{atype}` ')
	
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

	@commands.command(aliases=['information', 'botinfo'])
	async def info(self, ctx):
		msg = await ctx.send('Getting bot information ...')
		avgmembers = sum([guild.member_count for guild in self.bot.guilds]) / len(self.bot.guilds)
		ramPerc = psutil.virtual_memory().percent
		cpuUsage = psutil.cpu_percent(interval=0.5)
		cpuFreq = psutil.cpu_freq().current
		memory_usage = self.process.memory_full_info().uss / 1024**2
		cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

		pyVersion = platform.python_version()
		libVersion = get_distribution("discord.py").version
		hosting = platform.platform()

		emb = discord.Embed(colour=0x2F3136)
		#emb.set_thumbnail(url=self.bot.user.avatar_url)
		emb.set_author(name=self.bot.user.name, url='https://github.com/ppotatoo/pdbot', icon_url=self.bot.user.avatar_url)
		emb.set_thumbnail(url=self.bot.user.avatar_url)
		emb.add_field(name=f'Developer', value=f'```ppotatoo#6862 (777893499471265802)```', inline=False)
		emb.add_field(name=f'<:online:801444524148523088> Uptime', value=f'[Check Bot Status](https://stats.uptimerobot.com/Gzv84sJ9oV \"UptimeRobot\")\n```{humanize.precisedelta(self.bot.start_time, format="%0.0f")}```', inline=False)
		emb.add_field(name=f'Hosting', value=f'```{hosting}```', inline=False)

		emb.add_field(name=f'CPU Usage', value=f'```{cpu_usage:.2f}%```', inline=True)
		emb.add_field(name=f'CPU Frequency', value=f'```{cpuFreq} MHZ```', inline=True)
		emb.add_field(name='Memory Usage', value=f'```{ramPerc}%\n{memory_usage:.2f} MB```', inline=True)

		emb.add_field(name='<:python:801444523623710742> Python Version', value=f'```{pyVersion}```', inline=True)
		emb.add_field(name=f'<:discordpy:801444523854135307> Discord.py Version', value=f'```{libVersion}```', inline=True)

		emb.add_field(name='Command Count', value=f'```{len([x.name for x in self.bot.commands])} commands```', inline=False)
		emb.add_field(name='Guild Count', value=f'```{str(len(self.bot.guilds))} guilds```', inline=False)

		emb.add_field(name='Member Count', value=f'```{str(sum([guild.member_count for guild in self.bot.guilds]))} members```', inline=True)
		emb.add_field(name='Average Member Count', value=f'```{avgmembers:.1f}```')

		emb.set_footer(text=f'{ctx.author} • {ctx.author.id}', icon_url=ctx.author.avatar_url)

		await msg.edit(content=None, embed=emb)


def setup(bot):
	bot.add_cog(Misc(bot))