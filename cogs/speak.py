from discord.ext import commands
import discord

class example(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='send', help='hi')
	async def send(self, ctx, channel: discord.TextChannel, *, message):
		await self.channel.send(message) 
		await ctx.message.delete()


	@commands.command(name='say', help='Says something than deletes the message')
	async def say(ctx, *, message):
		await ctx.send(message)
		await ctx.message.delete()	


def setup(bot):
	bot.add_cog(example(bot))