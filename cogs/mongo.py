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
	
def setup(bot):
	bot.add_cog(mongo(bot))