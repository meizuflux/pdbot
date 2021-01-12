from discord.ext import commands
import discord
import json
import asyncio




class reactions(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.id == 766011729414062090:
			await message.add_reaction('<:shut:795701579876925480>')
		

def setup(bot):
	bot.add_cog(reactions(bot))