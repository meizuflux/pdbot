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
	async def zane_manip(self, ctx, image, method: str, fn: str):
		start = time.perf_counter()
		async with ctx.typing():
		# get the image
			if ctx.message.attachments:
				img = str(await ctx.message.attachments[0])
			elif isinstance(image, discord.PartialEmoji) or isinstance(image, discord.Emoji):
				img = str(await image.url.read())
			else:
				img = image or ctx.author
				img = str(img.avatar_url_as(static_format="png"))
			image = getattr(self.bot.zaneapi, method)
			m = await image(img)
			file = discord.File(m, filename=f"{fn}")
			end = time.perf_counter()
			embed = discord.Embed(colour=self.bot.embed_color)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://{fn}")
			embed.set_footer(text=f"Backend finished in {end-start:.2f} seconds")
			await ctx.send(embed=embed, file=file)
			await self.bot.zaneapi.close()


	

	@commands.command(help='This returns a gif of the image being increasingly content aware scaled')
	async def liquid(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='magic', fn='magik.gif')

	@commands.command(help='CAUTION: VERY SLOW This returns a gif of the image being bent like a bendy floor? You just have to see it for yourself.')
	async def floorgif(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='floor', fn='floor.gif')

	@commands.command()
	async def braille(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		async with ctx.typing():
			if ctx.message.attachments:
				img = str(await ctx.message.attachments[0])
			elif isinstance(image, discord.PartialEmoji):
				img = str(await image.url.read())
			else:
				img = image or ctx.author
				img = str(img.avatar_url_as(static_format="png"))
			image = await self.bot.zaneapi.braille(img)
			await ctx.send(image)

	@commands.command(help='Deepfry an image.')
	async def deepfry(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Emoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='deepfry', fn='deepfry.png')

	@commands.command(help='Recreate the image with overlapping black and white dots.')
	async def dots(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Emoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='dots', fn='dots.png')

	@commands.command(help='Compresses the image and strips it of any quality. Just like a JPEG.')
	async def jpeg(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Emoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='jpeg', fn='jpeg.jpeg')

	@commands.command(help='Animates spreading out all the pixels in the image giving a cool explosion-esque look.')
	async def spread(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Emoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='spread', fn='spread.gif')

	@commands.command(help='Makes a 3D looking cube out of the image.')
	async def cube(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Emoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='cube', fn='cube.png')

	@commands.command(help='Sort the pixels in the image.')
	async def sort(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Emoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='sort', fn='sorted.png')

	@commands.command(help='Image that takes up to 8 colors from the image and overlays their color and hex code to the side of the image.')
	async def palette(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Emoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='palette', fn='palleted.png')

	@commands.command(help='Posterize the image.')
	async def posterize(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Emoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='posterize', fn='posturized.png')

	@commands.command(help='Apply a sobel filter to the image.')
	async def sobel(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Emoji, discord.Member] = None):
		await self.zane_manip(self, ctx, image, method='sobel', fn='sobel.png')




		


def setup(bot):
	bot.add_cog(Zane(bot))