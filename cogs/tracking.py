from discord.ext import commands
import discord
import json

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
		if self.bot.user in message.mentions:
			with open("prefixes.json", "r") as f:
				prefix = json.load(f)
			await message.add_reaction('<:what:791007602745671701>')
			await message.channel.send(f"Hello <@{message.author.id}>, my prefix on this server is `{prefix[str(message.guild.id)]}`")

def setup(bot):
	bot.add_cog(tracking(bot))
