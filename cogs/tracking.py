from discord.ext import commands
import discord

class tracking(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot
		self.bot.counter = 0

	@commands.Cog.listener()
	async def on_command_completion(self, ctx):
		self.bot.counter += 1
		

	@commands.Cog.listener()
	async def on_message(self, message):
		if not message.guild:
			if message.author.id == self.bot.user.id:
				return
			else:
				channel = self.bot.get_channel(788471476927332382)
				creationtime = message.created_at
				embed = discord.Embed(title='*INCOMEING MESSAGE*', description=f'{message.author.mention} sent `{message.content}`', color=self.bot.embed_color)
				embed.set_thumbnail(url=message.author.avatar_url)
				embed.set_footer(text=f"Sent at {creationtime}	ID: {message.author.id}")
				embed.set_author(name=f'{message.author}', url='https://www.urbandictionary.com/define.php?term=Your%20mum%20gay', icon_url=f'{message.author.avatar_url}')
				await channel.send(embed=embed)
				return
		if message.content == '<@!777964578776285194>':
			prefix = await self.bot.prefix_db.pre.find_one({"_id": str(message.guild.id)})
			await message.add_reaction('<:what:791007602745671701>')
			e = discord.Embed(description=f'Hello {message.author.mention}, my prefix on this server is `{prefix["prefix"]}`. You can do `{prefix["prefix"]}help` to view all my commands.', color=self.bot.embed_color)
			await message.channel.send(embed=e)

def setup(bot):
	bot.add_cog(tracking(bot))
