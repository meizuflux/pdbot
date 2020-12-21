from discord.ext import commands
import discord

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='repeat', aliases=['copy', 'mimic'])
	async def do_repeat(self, ctx, *, our_input: str):
		await ctx.send(our_input)

	@commands.command(name='smolpp')
	async def smolpp(self, ctx, args):
		args = args.capitalize()
		if args == 'You' or args == 'I':
			await ctx.send(f'{args} have a smol pp')
		else: 
			await ctx.send(f'{args} has a smol pp')


def setup(bot):
	bot.add_cog(fun(bot))