from discord.ext import commands
import discord

class example(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='say')
	async def say(ctx, *, message: str):
		await ctx.send(message)
		await ctx.message.delete()
	
	@commands.command(name='dm', hidden=False)
	@commands.is_owner()
	async def pm(ctx: commands.Context, target: discord.User, *, message: str) -> None:
  		await target.send(message)


def setup(bot):
	bot.add_cog(example(bot))