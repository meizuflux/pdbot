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
	async def zane_manip(self, ctx, image, *, method: str):
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
			img = polaroid.Image(img)
			# manipulate the image
			img.resize(500, 500, 1)
			img = await self.bot.zaneapi.method(img)
			file = discord.File(BytesIO(img.save_bytes()), filename=f"{method}.png")
			end = time.perf_counter()
			embed = discord.Embed(colour=self.bot.embed_color)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://{method}.png")
			embed.set_footer(text=f"Backend finished in {end-start:.2f} seconds")
			await ctx.send(embed=embed, file=file)

	@commands.command(help='Pixelates an image')
	async def pixelate(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='pixelate')


def setup(bot):
	bot.add_cog(Zane(bot))