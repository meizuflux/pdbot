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

	def do_magic(img):
		i = Image(blob=avimg)
		i.format = 'jpg'
		i.liquid_rescale(width=int(i.width * 0.5),
									height=int(i.height * 0.5),
									delta_x=int(0.5 * 1),
									rigidity=0)
		i.liquid_rescale(width=int(i.width * 40),
									height=int(i.height * 1.5),
									delta_x=2,
									rigidity=0)
		byt = i.make_blob()
		im = polaroid.Image(byt)
		im.resize(500, 500, 1)
		file = discord.File(BytesIO(im.save_bytes()), filename="magik.jpg")
		return file

	@commands.command()
	async def magic(self, ctx, user: discord.Member=None):
		start = time.perf_counter()

		img = user or ctx.author
		avimg = BytesIO(await img.avatar_url_as(format="jpeg").read())

		thing = functools.partial(self.do_magic(), avimg)
		final = await self.bot.loop.run_in_executor(None, thing)

		emed=discord.Embed(title='You deserve this', color=self.bot.embed_color)
		emed.set_image(url='attachment://magik.jpg')
		end = time.perf_counter()
		emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')

		await ctx.send(embed=emed, file=final)


def setup(bot):
	bot.add_cog(wand(bot))