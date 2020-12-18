from discord.ext import commands
import discord

class fun(commands.Cog):
	def __init_(self, bot):
		self.bot = bot

	@commands.command(name='repeat', aliases=['copy', 'mimic'])
	async def do_repeat(self, ctx, *, our_input: str):
		await ctx.send(our_input)

def setup(bot):
	bot.add_cog(fun(bot))