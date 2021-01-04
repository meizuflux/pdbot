from discord.ext import commands
import discord
import json


with open("data.json", "r") as f:
		data = json.load(f)

class reactions(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.id == 766011729414062090 and 'no' in message.content:
			await message.delete()
		if message.author.id == 766011729414062090:
			await message.add_reaction('<:shut:795701579876925480>')
		if self.bot.user in message.mentions:
			await message.add_reaction('<:what:791007602745671701>')
			await message.channel.send(f"Hello <@{message.author.id}>, my prefix on this server is `{data['prefix']}`")
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