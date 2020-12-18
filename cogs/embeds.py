from discord.ext import commands
import discord

class embeds(commands.Cog):
	def __init_(self, bot):
		self.bot = bot

	@commands.command(name='exembed', help='the name')
	async def embedserino(ctx):
		creationtime = ctx.message.created_at
		embed = discord.Embed(title = 'Test Embed', description = 'hello world')
		embed.colour = 0xFFFFFF  # can be set in 'discord.Embed()' too

		# Images
		embed.set_image(url = 'https://i.imgur.com/GPYcrdB.jpeg')
		embed.set_thumbnail(url = 'https://i.imgur.com/GPYcrdB.jpeg')

		embed.set_author(name = 'Author name', url = 'google.com', icon_url = 'https://i.imgur.com/GPYcrdB.jpeg') # appears on top
		embed.set_footer(text = 'Example footer', icon_url = 'https://i.imgur.com/GPYcrdB.jpeg') 
		embed.timestamp = creationtime 
		embed.add_field(name = 'Name [256 char max]', value = 'Content [1024 char]', inline=True) 
		# max 25 fields

def setup(bot):
	bot.add_cog(embeds(bot))