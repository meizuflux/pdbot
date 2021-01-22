from discord.ext import commands
import discord
import polaroid
import functools
import typing
from io import BytesIO

class image(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@staticmethod
	async def manip(ctx, image, *, method: str, method_args: list = None, text: str = None):
		async with ctx.typing():
		# get the image
			if ctx.message.attachments:
				img = polaroid.Image(await ctx.message.attachments[0].read())
			elif isinstance(image, discord.PartialEmoji):
				img = polaroid.Image(await image.url.read())
			else:
				img = image or ctx.author
				img = polaroid.Image(await img.avatar_url_as(format="png").read())
			# manipulate the image
			if method_args is None:
			        method_args = []
			method = getattr(img, method)
			method(*method_args)
			file = discord.File(BytesIO(img.save_bytes()), filename=f"polaroid.png")
			embed = discord.Embed(description=text, colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://polaroid.png")
			embed.set_footer(text=f"Powered by Polaroid")
			await ctx.send(embed=embed, file=file)

	@commands.command(help='Makes an image rainbowey')
	async def rainbow(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='apply_gradient')

	@commands.command(help='like putin')
	async def wide(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='resize', method_args=(2000, 900, 1), text='ｗｉｄｅ')

	@commands.command(help='Rotates an image sideways')
	async def sideways(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='rotate90')

	@commands.command(help='Rotates an image sideways')
	async def upsidedown(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='rotate180')

	@commands.command(help='me learning how to use executors', hidden=True)
	async def exec(self, ctx, width: int=None, height: int=None):
		byt = await ctx.author.avatar_url_as(format="png").read()
		
		def sync_func():
			im = polaroid.Image(byt)
			im.resize(1800, 900, 1)
			file = discord.File(BytesIO(im.save_bytes()), filename=f"stretched.png")
			return file

		async def async_func():
			thing = functools.partial(sync_func)
			file = await self.bot.loop.run_in_executor(None, thing)
			await ctx.send('ｗｉｄｅ', file=file)

		await async_func()



def setup(bot):
	bot.add_cog(image(bot))