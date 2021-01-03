from discord.ext import commands
import discord
import random

class tracking(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if not message.guild:
			if message.author.id == self.bot.user.id:
				return
			else:
				channel = self.bot.get_channel(788471476927332382)
				creationtime = message.created_at
				embed = discord.Embed(title='*INCOMEING MESSAGE*', description=f'{message.author.mention} sent `{message.content}`')
				embed.colour = 0xFFFFFF
				embed.set_thumbnail(url=message.author.avatar_url)
				embed.set_footer(text=f"Sent at {creationtime}	ID: {message.author.id}")
				embed.set_author(name=f'{message.author}', url='https://www.urbandictionary.com/define.php?term=Your%20mum%20gay', icon_url=f'{message.author.avatar_url}')
				await channel.send(embed=embed)
				return

	@commands.Cog.listener()
	async def on_command(self, ctx):
		channel = self.bot.get_channel(788471476927332382)
		embed2 = discord.Embed(title='Command Use')
		embed2.color = discord.Colour.from_hsv(random.random(), 1, 1) #0x2f3136 is the gray color that blends in
		#embed2.set_thumbnail(url=ctx.author.avatar_url)
		embed2.set_footer(text=f"Sent at {ctx.message.created_at}")
		embed2.add_field(name='Command', value=f'{ctx.message.content}', inline=False)
		embed2.add_field(name='Where', value=f'#{ctx.channel}, ID = {ctx.channel.id}, Guild = {ctx.guild}')
		embed2.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed2.set_footer(text=f'Sent at {ctx.message.created_at}')

		await channel.send(embed=embed2)

def setup(bot):
	bot.add_cog(tracking(bot))
