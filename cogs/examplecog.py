from discord.ext import commands
import discord

class examplecog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='whatsgood')
	async def helloworld(self, ctx):
		await ctx.send('HELLO WHATS GOOD MY DUDES LETS GOOOOO')

	@commands.command(name='astrelladies')
	async def fakeembed(self, ctx):
		embed = discord.Embed(title='he ded', description='can we get an f in the chat')
		embed.colour = 0xFFFFFF  # can be set in 'discord.Embed()' too
		embed.set_image(url='https://media.discordapp.net/attachments/786309313786019891/790598215137099807/tenor_2.gif')

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(examplecog(bot))