from discord.ext import commands
import discord
import json

with open("data.json", "r") as f:
		data = json.load(f)
class testingjson(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='prefix')
	@commands.has_role('MANAGER')
	async def prefix(self, ctx, args):
		data["prefix"] = args
		with open("data.json", "w") as f:
			json.dump(data, f, indent=4)
		await ctx.send(f'Set prefix to ' +data['prefix'])


	@commands.command(name='testprefix', hidden=True)
	@commands.has_role('MANAGER')
	async def testprefix(self, ctx, args):
		tonk = ctx.guild.name
		data[tonk] = args
		with open("data.json", "w") as f:
			json.dump(data, f, indent=4)
		await ctx.send(f'Set prefix to ' +data[tonk]+' in this server')
		



def setup(bot):
	bot.add_cog(testingjson(bot))