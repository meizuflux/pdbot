from discord.ext import commands
import discord
import utils.embed as qembed

class Economy(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot
		self.bot.eco = self.bot.data.economy

	@commands.command(help='Registers you into the database')
	async def register(self, ctx):
		try:
			await self.bot.eco.insert_one({"_id": ctx.author.id, "wallet": 100, "bank": 0})
			await qembed.send(ctx, 'Sucessfully registered you!')
		except:
			await qembed.send(ctx, 'You are already registered!')

	@commands.command(help='View yours or someone elses balance')
	async def bal(self, ctx, user: discord.Member = None):
		data = await self.bot.eco.find_one({"_id": user.id if user else ctx.author.id})
		e = discord.Embed(title=f'{user.name if user else ctx.author.name}\'s balance', description=f'<:member_join:596576726163914752> **Wallet**: {data["wallet"]}\n<:member_join:596576726163914752> **Bank**: {data["bank"]}\n<:member_join:596576726163914752> **Total**: {data["wallet"] + data["bank"]}', color=self.bot.embed_color)
		e.set_thumbnail(url=user.avatar_url if user else ctx.author.avatar_url)
		await ctx.send(embed=e)


def setup(bot):
	bot.add_cog(Economy(bot))