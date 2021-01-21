from discord.ext import commands
import discord

class example(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='say')
	@commands.is_owner()
	async def say(self, ctx, *, message: str):
		await ctx.send(message)
		await ctx.message.delete()
	
	@commands.command(name='dm', hidden=False)
	@commands.is_owner()
	async def pm(self, ctx, target: discord.User, *, message: str):
  		await target.send(message)


def setup(bot):
	bot.add_cog(example(bot))