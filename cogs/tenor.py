from discord.ext import commands
import discord
import random
import TenGiphPy
import os
ttoken = os.environ['tenortoken']
gtoken = os.environ['giphytoken']

tokens = {'tenor': ttoken,
          'giphy': gtoken}
t = TenGiphPy.Tenor(token=tokens['tenor'])
g = TenGiphPy.Giphy(token=tokens['giphy'])

class Tenor(commands.Cog, name='Tenor Commands', command_attrs=dict(hidden=False)):
	"""Collection of commands which draw GIFs from Tenor"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='smack', help='!smack <person>')
	async def smack(self, ctx, args):
		if len(args) == 0:
			return
		else:
			if self.bot.user in ctx.message.mentions:
				await ctx.send('Fuck you')
			else:
				embed = discord.Embed(description=f'**<@{ctx.author.id}> smacks {args}! <:POGGER:790605271898259516>**')
				embed.color = 0x2f3136
				embed.set_image(url=t.random("anime smack"))
				await ctx.send(embed=embed)
    

	@commands.command(name='cute', help='!cute <person>')
	async def cute(self, ctx, args):
		if len(args) == 0:
			return
		else:
			cuteembed = discord.Embed(description=f'🎉 <@{ctx.author.id}> calls {args} cute! <:woah:790662057141731378>')
			cuteembed.color = 0x2f3136
			cuteembed.set_image(url=t.random("anime cute"))
			await ctx.send(embed=cuteembed)

	@commands.command(name='hug', help='!hug <person>')
	async def hug(self, ctx, args):
		hugtype = ['anime hug','anime cute hug','hug']
		if len(args) == 0:
			return
		else:
			hugembed = discord.Embed(description=f'🎉 <@{ctx.author.id}> hugs {args}! <:floshed:790667091022708757>')
			hugembed.set_image(url=t.random(f"{random.choice(hugtype)}"))
			hugembed.color = 0x2f3136
			await ctx.send(embed=hugembed)


	@commands.command(name='kiss', help='!kiss <person>')
	async def kiss(self, ctx, member: str):
		kisstype = ['anime kiss','anime cute kiss','kiss']
		hugembed = discord.Embed(description=f'🎉 <@{ctx.author.id}> kisses {member}! <:floshed:790667091022708757>')
		hugembed.set_image(url=t.random(f"{random.choice(kisstype)}"))
		hugembed.color = 0x2f3136
		await ctx.send(embed=hugembed)

def setup(bot):
	bot.add_cog(Tenor(bot))

