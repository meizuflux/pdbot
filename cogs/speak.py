from discord.ext import commands
import discord
import asyncio

class speak(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='say')
	@commands.is_owner()
	async def say(self, ctx, *, message: str):
		await ctx.send(message)
		try:
			await ctx.message.delete()
		except discord.Forbidden:
			pass
	
	@commands.command(name='dm')
	@commands.is_owner()
	async def pm(self, ctx, target: discord.User, *, message: str):
  		await target.send(message)

	@commands.command()
	@commands.is_owner()
	async def send(self, ctx, chid: int, *, message):
		async with ctx.typing():
			tonk = len(message) * 0.15
			await asyncio.sleep(tonk)
			channel = self.bot.get_channel(chid)
			await channel.send(message)


def setup(bot):
	bot.add_cog(speak(bot))