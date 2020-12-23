from discord.ext import commands
import discord
import json

class testingjson(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot

	with open("data.json", "r") as f:
		data = json.load(f)

	@commands.command(name='cutetest')
	async def cute(self, ctx, *, message):
		with open("data.json", "r") as f:
			data = json.load(f)
			data["cute"] = message
		with open("data.json", "w") as f:
			json.dump(data, f, indent=4)
		await ctx.send(data['cute'])

	@commands.command(name='prefix')
	@commands.has_role('MANAGER')
	async def prefix(self, ctx, args):
		with open("data.json", "r") as f:
			data = json.load(f)
		data["prefix"] = args
		with open("data.json", "w") as f:
			json.dump(data, f, indent=4)
		await ctx.send(f'Set prefix to ' +data['prefix'])



def setup(bot):
	bot.add_cog(testingjson(bot))