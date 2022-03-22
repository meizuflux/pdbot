from discord.ext import commands
import discord
import json
import utils.embed as qembed

class prefixes(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot
		self.bot.prefix_db = self.bot.mongo.prefixes

    
	def mng_gld():
		def predicate(ctx):
			if ctx.author.id == ctx.bot.author_id:
				return True
			return ctx.author.guild_permissions.manage_guild == True
		return commands.check(predicate)

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		await self.bot.prefix_db.pre.insert_one({"_id": guild.id}, {"prefix": "c//"})
		await self.bot.db.execute("INSERT INTO prefixes(serverid,prefix) VALUES($1,$2) ON CONFLICT (serverid) DO UPDATE SET prefix = $2", guild.id, self.bot.default_prefix)
		self.bot.prefixes.pop(guild.id, None)


	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		await self.bot.prefix_db.pre.delete_one({"_id": guild.id})
		await self.bot.db.execute("DELETE FROM prefixes WHERE serverid = $1", guild.id)
		self.bot.prefixes[guild.id] = self.bot.default_prefix

	@commands.command(help='Changes the bots prefix')
	@mng_gld()
	async def mongoprefix(self, ctx, *, prefix):
		await self.bot.prefix_db.pre.replace_one({"_id": ctx.guild.id}, {"prefix": prefix})
		prefix = await self.bot.prefix_db.pre.find_one({"_id": ctx.guild.id})
		await qembed.send(ctx, f'Changed prefix to `{prefix["prefix"]}` successfully.')

	@commands.command(aliases=['changeprefix', 'setprefix'])
	@mng_gld()
	async def prefix(self, ctx, prefix):
	    await self.bot.db.execute("INSERT INTO prefixes(serverid,prefix) VALUES($1,$2) ON CONFLICT (serverid) DO UPDATE SET prefix = $2",ctx.guild.id, prefix)
	    self.bot.prefixes[ctx.guild.id] = prefix
	    await qembed.send(ctx, f"Changed prefix to `{prefix}`")

	@commands.command(help='Shows the prefix for this server', aliases=['serverprefix'])
	async def botprefix(self, ctx):
		if not ctx.guild:
			await qembed.send(ctx, 'My prefix is `c//`')
		else:
			prefix = await self.bot.prefix_db.pre.find_one({"_id": ctx.guild.id})
			await qembed.send(ctx, f'My prefix on this server is `{prefix["prefix"]}`')

def setup(bot):
	bot.add_cog(prefixes(bot))