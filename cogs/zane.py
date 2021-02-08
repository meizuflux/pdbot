from discord.ext import commands
import discord
import os
import polaroid
import typing
import aiozaneapi
from io import BytesIO
import time

zane_api = os.environ['zanekey']

class Zane(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot
		self.bot.zaneapi = aiozaneapi.Client(zane_api)

	@staticmethod
	async def zane_manip(self, ctx, image, method):
		client = aiozaneapi.Client(zane_api)
		start = time.perf_counter()
		async with ctx.typing():
		# get the image
			if ctx.message.attachments:
				img = BytesIO(await ctx.message.attachments[0].read())
			elif isinstance(image, discord.PartialEmoji):
				img = BytesIO(await image.url.read())
			else:
				img = image or ctx.author
				img = BytesIO(await img.avatar_url_as(format="png").read())
			img = getattr(client, method(img))
			img = await self.bot.zaneapi.pixelate(img)
			file = discord.File(BytesIO(img.save_bytes()), filename=f"{method}.png")
			end = time.perf_counter()
			embed = discord.Embed(colour=self.bot.embed_color)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://{method}.png")
			embed.set_footer(text=f"Backend finished in {end-start:.2f} seconds")
			await ctx.send(embed=embed, file=file)

	@commands.command(help='Pixelates an image')
	async def pixelate(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		start = time.perf_counter()
		async with ctx.typing():
		# get the image
			if ctx.message.attachments:
				img = str(await ctx.message.attachments[0].url)
			elif isinstance(image, discord.PartialEmoji):
				img = str(await image.url)
			else:
				img = image or ctx.author
				img = str(img.avatar_url_as(static_format="png"))
			#img = getattr(client, method(img))
			img = await self.bot.zaneapi.pixelate(img)
			file = discord.File(fp=img, filename=f"zane.gif")
			end = time.perf_counter()
			embed = discord.Embed(colour=self.bot.embed_color)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://zane.gif")
			embed.set_footer(text=f"Backend finished in {end-start:.2f} seconds")
			await ctx.send(embed=embed, file=file)


def setup(bot):
	bot.add_cog(Zane(bot))