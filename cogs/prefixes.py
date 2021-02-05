from discord.ext import commands
import discord
import json
import utils.embed as qembed

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
		await self.bot.prefix_db.pre.insert_one({"_id": str(guild.id)}, {"prefix": "c//"})

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		await self.bot.prefix_db.pre.delete_one({"_id": str(guild.id)})

	@commands.command(help='Changes the bots prefix', aliases=['setprefix'])
	@mng_gld()
	async def prefix(self, ctx, *, prefix):
		await self.bot.prefix_db.pre.replace_one({"_id": str(ctx.guild.id)}, {"prefix": prefix})
		prefix = await self.bot.prefix_db.pre.find_one({"_id": str(ctx.guild.id)})
		await qembed.send(ctx, f'Changed prefix to `{prefix["prefix"]}` successfully.')

	@commands.command(help='Shows the prefix for this server', aliases=['serverprefix'])
	async def botprefix(self, ctx):
		if not ctx.guild:
			await qembed.send(ctx, 'My prefix is `c//`')
		else:
			prefix = await self.bot.prefix_db.pre.find_one({"_id": str(ctx.guild.id)})
			await qembed.send(ctx, f'My prefix on this server is `{prefix["prefix"]}`')

def setup(bot):
	bot.add_cog(prefixes(bot))