from discord.ext import commands
import discord
import os
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MongoDB'])

db = client.prefixes #prefixes is the collection name
users = client.users



class mongo(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.is_owner()
	async def mongoprefix(self, ctx, *, test: str):
		await db.pre.replace_one({"_id": str(ctx.guild.id)}, {"prefix": test})
		prefix = await db.pre.find_one({"_id": str(ctx.guild.id)})
		e = discord.Embed(description=f'Changed prefix to `{prefix["prefix"]}` successfully.', color=self.bot.embed_color)
		await ctx.send(embed=e)

	@commands.command()
	async def getmongo(self, ctx):
		prefix = await db.pre.find_one({"_id": str(ctx.guild.id)})
		await ctx.send(prefix['prefix'])

	@commands.command()
	async def mongoregister(self, ctx, favorite_color: str):
		await users.user.insert_one({"_id": str(ctx.author.id), "name": str(ctx.author.name), "favorite color": favorite_color})
		await ctx.send('registered u')

	@commands.command()
	async def mongoupdate(self, ctx, favorite_color: str):
		await users.user.replace_one({"_id": str(ctx.author.id)}, {"favorite color": favorite_color})
		await ctx.send('yea I updated you loser')

	@commands.command()
	async def mongocolor(self, ctx, user: discord.Member=None):
		if not user:
			user = ctx.author
		prefix = await users.user.find_one({"_id": str(user.id)})
		await ctx.send(prefix['favorite color'])
	
def setup(bot):
	bot.add_cog(mongo(bot))