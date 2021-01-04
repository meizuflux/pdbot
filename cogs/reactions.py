from discord.ext import commands
import discord

class reactions(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if self.bot.user in message.mentions:
			await message.add_reaction('<:what:791007602745671701>')
		await message.add_reaction('<:SantaGiggle:795701579578605599>')
		if message.channel.id == int(789329010080743444):
			await message.add_reaction('\N{UPWARDS BLACK ARROW}')
			await message.add_reaction('\N{DOWNWARDS BLACK ARROW}')
		if message.channel.id == int(788058309973901344):
			await message.add_reaction('\N{UPWARDS BLACK ARROW}')
			await message.add_reaction('\N{DOWNWARDS BLACK ARROW}')
		if message.channel.id == int(769195542026125373):
			await message.add_reaction('\N{UPWARDS BLACK ARROW}')
			await message.add_reaction('\N{DOWNWARDS BLACK ARROW}')


def setup(bot):
	bot.add_cog(reactions(bot))