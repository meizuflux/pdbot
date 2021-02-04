from discord.ext import commands
import discord
from wand.image import Image
import wand, wand.color, wand.drawing
from io import BytesIO
import polaroid
import time
import functools

class wand(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	

	@commands.command()
	async def magic(self, ctx, user: discord.Member=None, scale: int=None):
		start = time.perf_counter()

		img = user or ctx.author
		avimg = BytesIO(await img.avatar_url_as(format="jpeg").read())
		def do_magic():
			i = Image(blob=avimg)
			i.format = 'jpg'
			i.liquid_rescale(width=int(i.width * 0.5),
								height=int(i.height * 0.5),
								delta_x=int(0.5 * scale) if scale else 1,
								rigidity=0)
			i.liquid_rescale(width=int(i.width * 1.5),
								height=int(i.height * 1.5),
								delta_x=scale if scale else 2,
								rigidity=0)
			byt = i.make_blob()
			im = polaroid.Image(byt)
			im.resize(500, 500, 1)
			file = discord.File(BytesIO(im.save_bytes()), filename="magik.jpg")
			return file
		final = await self.bot.loop.run_in_executor(None, do_magic)

		emed=discord.Embed(title='mAgiK', color=self.bot.embed_color)
		emed.set_image(url='attachment://magik.jpg')
		end = time.perf_counter()
		emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')

		await ctx.send(embed=emed, file=final)

	@commands.command()
	async def floor(self, ctx, user: discord.Member=None):
		start = time.perf_counter()

		img = user or ctx.author
		avimg = BytesIO(await img.avatar_url_as(format="jpeg").read())
		def do_magic():
			i = Image(blob=avimg)
			i.format = 'jpg'
			#thanks daggy https://github.com/daggy1234/dagpi-image
			i.resize(250, 250)
			x, y = i.width, i.height
			arguments = (0, 0, 77, 153, x, 0, 179, 153, 0, y, 51, 255, x, y, 204, 255)
			i.distort("perspective", arguments)
			byt = i.make_blob()
			im = polaroid.Image(byt)
			im.resize(500, 500, 1)
			file = discord.File(BytesIO(im.save_bytes()), filename="magik.jpg")
			return file
		final = await self.bot.loop.run_in_executor(None, do_magic)

		emed=discord.Embed(title='see the floor losers', color=self.bot.embed_color)
		emed.set_image(url='attachment://magik.jpg')
		end = time.perf_counter()
		emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')

		await ctx.send(embed=emed, file=final)


def setup(bot):
	bot.add_cog(wand(bot))