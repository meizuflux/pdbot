from discord.ext import commands
import discord
import json

class prefixes(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot
    
	def mng_gld():
		def predicate(ctx):
			if ctx.author.id == ctx.bot.author_id:
				return True
			if ctx.author.guild_permissions.manage_guild == True:
				return True
			else: 
				return False
		return commands.check(predicate)

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

		prefixes[str(guild.id)] = 'c//'

		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

		prefixes.pop(str(guild.id))

		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)

	@commands.command(name='prefix')
	@mng_gld()
	async def prefix(self, ctx, prefix: str):
		if len(prefix) > 5:
			await ctx.send('Prefixes must be under 5 characters!')
		else:
			with open('prefixes.json', 'r') as f:
				prefixes = json.load(f)

			prefixes[str(ctx.guild.id)] = prefix

			with open('prefixes.json', 'w') as f:
				json.dump(prefixes, f, indent=4)
			await ctx.send(f'Set prefix to {prefixes[str(ctx.guild.id)]}')


	@prefix.error
	async def prefix_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('You need manage guild permissions in order to change the prefix. The prefix on this server is '+prefixes[str(ctx.guild.id)])

def setup(bot):
	bot.add_cog(prefixes(bot))