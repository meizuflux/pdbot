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

	@commands.command(name='smack', help='Smack someone')
	async def smack(self, ctx, user):	
		embed = discord.Embed(description=f'**<@{ctx.author.id}> smacks {user}! <:POGGER:790605271898259516>**', color=self.bot.embed_color)
		embed.set_image(url=t.random("anime smack"))
		await ctx.send(embed=embed)
    

	@commands.command(name='cute', help='Call a person cute')
	async def cute(self, ctx, user):
		cuteembed = discord.Embed(description=f'🎉 <@{ctx.author.id}> calls {user} cute! <:woah:790662057141731378>', color=self.bot.embed_color)
		cuteembed.set_image(url=t.random("anime cute"))
		await ctx.send(embed=cuteembed)

	@commands.command(name='hug', help='Hugs someone')
	async def hug(self, ctx, user):
		hugtype = ['anime hug','anime cute hug','hug']
		hugembed = discord.Embed(description=f'🎉 <@{ctx.author.id}> hugs {user}! <:floshed:790667091022708757>', color=self.bot.embed_color)
		hugembed.set_image(url=t.random(f"{random.choice(hugtype)}"))
		await ctx.send(embed=hugembed)


	@commands.command(help='Kisses someone')
	async def kiss(self, ctx, user):
		kisstype = ['anime kiss','anime cute kiss','kiss']
		hugembed = discord.Embed(description=f'🎉 <@{ctx.author.id}> kisses {user}! <:floshed:790667091022708757>', color=self.bot.embed_color)
		hugembed.set_image(url=t.random(f"{random.choice(kisstype)}"))
		await ctx.send(embed=hugembed)

def setup(bot):
	bot.add_cog(Tenor(bot))

