from discord.ext import commands
import discord

class examplecog(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='hello')
	async def helloworld(self, ctx):
		await ctx.send(f'Hello! My name is {ctx.bot.user.nick}')

def setup(bot):
	bot.add_cog(examplecog(bot))