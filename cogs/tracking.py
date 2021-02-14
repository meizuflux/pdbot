from discord.ext import commands
import discord

class tracking(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot
		self.bot.counter = 0
		self.bot.snipes = {}
		self.bot.edits = {}
		self.context = None

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		self.bot.snipes[message.channel.id] = message
		self.bot.snipes[message.author.id] = message


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

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		self.bot.edits[before.channel.id] = before
		self.bot.edits[before.author.id] = before
		if before.author.id == self.bot.author_id and not before.embeds and not after.embeds:
			await self.bot.process_commands(after)

def setup(bot):
	bot.add_cog(tracking(bot))
