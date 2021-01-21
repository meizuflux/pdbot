from discord.ext import commands
import discord
import polaroid
import functools
from io import BytesIO

class image(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@staticmethod
	async def do_img_manip(ctx, image, *, method: str, filename: str):
		def manip():
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
					method_args = []
					method_kwargs = {}
					method = getattr(img, method)
					method(*method_args, **method_kwargs)
					file = discord.File(BytesIO(img.save_bytes()), filename=f"{filename}.png")
					return file
		async def emb():
			thing = functools.partial(manip)
			file = await self.bot.loop.run_in_executor(None, thing)
			embed = discord.Embed()
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://{filename}.png")
			await ctx.send(embed=embed, file=file)
		await emb()

	@commands.command()
	async def stretch(self, ctx):
		byt = await ctx.author.avatar_url_as(format="png").read()
		
		def sync_func():
			im = polaroid.Image(byt)
			w,h = im.size
			file = discord.File(BytesIO(im.save_bytes()), filename=f"stretched.png")
			return file

		async def async_func():
			thing = functools.partial(sync_func)
			file = await self.bot.loop.run_in_executor(None, thing)
			await ctx.send('And your image is here', file=file)

		await async_func()



def setup(bot):
	bot.add_cog(image(bot))