from discord.ext import commands
import discord
import json

class testingjson(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot

	with open("test.json", "r") as f:
		data = json.load(f)

	@commands.command(name='cutetest')
	async def cute(self, ctx, *, message):
		with open("test.json", "r") as f:
			data = json.load(f)
			data["cute"] = message
		with open("data.json", "w") as f:
			json.dump(data, f, indent=4)
		await ctx.send(data['cute'])



def setup(bot):
	bot.add_cog(testingjson(bot))