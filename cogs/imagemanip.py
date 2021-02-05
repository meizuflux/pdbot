from discord.ext import commands
import discord
import polaroid
import functools
import typing
import os
import wand, wand.color, wand.drawing
from wand.image import Image as WandImage
import time
from PIL import Image
from asyncdagpi import ImageFeatures
from io import BytesIO
flipnotetoken = os.environ['tflipnote']

class image(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#thanks PB https://github.com/PB4162/PB-Bot
	@staticmethod
	async def manip(self, ctx, image, *, method: str, method_args: list = None, text: str = None):
		start = time.perf_counter()
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
			img.resize(500, 500, 1)
			if method_args is None:
			        method_args = []
			method = getattr(img, method)
			method(*method_args)
			file = discord.File(BytesIO(img.save_bytes()), filename="polaroid.png")
			end = time.perf_counter()
			embed = discord.Embed(description=text, colour=self.bot.embed_color)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://polaroid.png")
			embed.set_footer(text=f"Backend finished in {end-start:.2f} seconds")
			await ctx.send(embed=embed, file=file)

	async def alex_image(self, url):
		async with self.bot.session.get(f'https://api.alexflipnote.dev/{url}', headers={'Authorization': flipnotetoken}) as r:
			io = BytesIO(await r.read())
			f = discord.File(fp=io, filename='alex.png')
			return f

	@commands.command(aliases=['didyoumean'], help='"Did you mean" meme. Ex: dym "milk" "with your dad"')
	async def dym(self, ctx, search: str, did_you_mean: str):
		file = await self.alex_image(url=f'didyoumean?top={search}&bottom={did_you_mean}')
		embed = discord.Embed(colour=self.bot.embed_color)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_image(url="attachment://alex.png")
		embed.set_footer(text="Powered by the AlexFlipnote API")
		await ctx.send(embed=embed, file=file)

	@commands.command(aliases=['trigger'], help='Makes you or a user TRIGGERED')
	async def triggered(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		async with ctx.typing():
			#if ctx.message.attachments: busted rn
				#url = str(ctx.message.attachments[0].url)
			if isinstance(image, discord.PartialEmoji):
				url = str(image.url)
			else:
				img = image or ctx.author
				url = str(img.avatar_url_as(static_format='png', format='png', size=512))
			img = await self.bot.dagpi.image_process(ImageFeatures.triggered(), url)
			file = discord.File(fp=img.image,filename=f"triggered.{img.format}")
			embed = discord.Embed(colour=self.bot.embed_color)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://triggered.gif")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)
			# await self.imgemb(ctx, dfile=file, footername='triggered.gif', powered='the Dagpi API') currently file doesn't send

	@commands.command(aliases=['magik'], help='Warps an image. You can also choose the scale.')
	async def magic(self, ctx, user: discord.Member=None, scale: int=None):
		start = time.perf_counter()

		img = user or ctx.author
		avimg = BytesIO(await img.avatar_url_as(format="jpeg").read())
		def do_magic():
			i = WandImage(blob=avimg)
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

	@commands.command(help='Some weird perspective stuff')
	async def floor(self, ctx, user: discord.Member=None):
		start = time.perf_counter()

		img = user or ctx.author
		avimg = BytesIO(await img.avatar_url_as(format="jpeg").read())
		def do_magic():
			i = WandImage(blob=avimg)
			i.format = 'jpg'
			#thanks daggy https://github.com/daggy1234/dagpi-image
			i.virtual_pixel = "mirror"
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

	

	@commands.command(help='Overlays the communist logo on a users PFP')
	async def slowcommunist(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		async with ctx.typing():
			#if ctx.message.attachments: busted rn
				#url = str(ctx.message.attachments[0].url)
			if isinstance(image, discord.PartialEmoji):
				url = str(image.url)
			else:
				img = image or ctx.author
				url = str(img.avatar_url_as(static_format='jpeg', format='jpeg', size=512))
			img = await self.bot.dagpi.image_process(ImageFeatures.communism(), url)
			file = discord.File(fp=img.image,filename=f"communism.{img.format}")
			embed = discord.Embed(colour=self.bot.embed_color)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://communism.gif")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)	

	@commands.command(help='Creates a fake tweet')
	async def twitter(self, ctx, user: discord.Member, *, text: str):
		async with ctx.typing():
			url = str(user.avatar_url_as(static_format='png', format='png', size=512))
			disname = user.display_name
			name = disname.replace(' ', '')
			img = await self.bot.dagpi.image_process(ImageFeatures.tweet(), text=text, url=url, username=name)
			file = discord.File(fp=img.image,filename=f"tweet.{img.format}")
			embed = discord.Embed(colour=self.bot.embed_color)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://tweet.png")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)
			
	@commands.command(name='5g1g', help='The five guys one girl meme')
	async def fgog(self, ctx, user1: discord.Member, user2: discord.Member):
		async with ctx.typing():
			url = str(user1.avatar_url_as(static_format='png', format='png', size=512))
			url2 = str(user2.avatar_url_as(static_format='png', format='png', size=512))
			img = await self.bot.dagpi.image_process(ImageFeatures.five_guys_one_girl(), url=url, url2=url2)
			file = discord.File(fp=img.image,filename=f"five_guys_one_girl.{img.format}")
			embed = discord.Embed(colour=self.bot.embed_color)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://five_guys_one_girl.png")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)

	@commands.command(help='Makes an image rainbowey')
	async def rainbow(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='apply_gradient')

	@commands.command(help='Stretches an image')
	async def wide(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='resize', method_args=(2000, 900, 1), text='ｗｉｄｅ')

	@commands.command(help='Inverts an image')
	async def invert(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='invert')

	@commands.command(help='It\'s like looking in a mirror')
	async def flip(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='fliph')

	@commands.command(help='Blurs an image? Duh')
	async def blur(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='box_blur')

	@commands.command(help='Don\'t really know what this is, but its scary')
	async def sobelh(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='sobel_horizontal')

	@commands.command(help='cursed')
	async def sobelv(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='sobel_vertical')

	@commands.command(help='Decomposes the image')
	async def decompose(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='decompose_max')

	@commands.command(help='Turns an image black and white')
	async def grayscale(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='grayscale')
		
	@commands.command(help='Solarizes an image')
	async def solarize(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='solarize')
		
	@commands.command(help='Rotates an image sideways')
	async def sideways(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='rotate90')

	@commands.command(help='Rotates an image upsidedown', example='upsidedown person')
	async def upsidedown(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(self, ctx, image, method='rotate180')

	@commands.command(help='makes an image communist', aliases=['communism'])
	async def communist(self, ctx, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		start = time.perf_counter()
		async with ctx.typing():
			if ctx.message.attachments:
				avimg = BytesIO(await ctx.message.attachments[0].read())
			elif isinstance(image, discord.PartialEmoji):
				avimg = BytesIO(await image.url.read())
			else:
				img = image or ctx.author
				avimg = BytesIO(await img.avatar_url_as(format="png").read())

			def sync_func():
				image = Image.open(avimg)
				image = image.resize((500, 500))
				ci = image.convert("RGBA")
				file = Image.open("assets/cropflag.png")
				file = file.convert("RGBA")
				file = file.resize((500, 500))
				blend = Image.blend(ci, file, 0.5)
				byt = BytesIO()
				blend.save(byt, format='png')
				byt.seek(0)
				file = discord.File(fp=byt, filename="communism.png")
				return file

			async def async_func():
				thing = functools.partial(sync_func)
				file = await self.bot.loop.run_in_executor(None, thing)
				end = time.perf_counter()
				emed=discord.Embed(title='Communism', color=self.bot.embed_color)
				emed.set_image(url='attachment://communism.png')
				emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')
				await ctx.send(embed=emed, file=file)
			await async_func()

	@commands.command(help='blends two users together', aliases=['mesh'])
	async def blend(self, ctx, image1: typing.Union[discord.PartialEmoji, discord.Member], image2: typing.Union[discord.PartialEmoji, discord.Member] = None):
		start = time.perf_counter()
		async with ctx.typing():
			if isinstance(image1, discord.PartialEmoji):
				img1 = BytesIO(await image1.url.read())
			else:
				img1 = BytesIO(await image1.avatar_url_as(format="png").read())

			if isinstance(image2, discord.PartialEmoji):
				img2 = BytesIO(await image2.url.read())
			else:
				img = image2 or ctx.author
				img2 = BytesIO(await img.avatar_url_as(format="png").read())
			def sync_func():
				image = Image.open(img1)
				image = image.resize((500, 500))
				ci = image.convert("RGBA")
				file = Image.open(img2)
				file = file.convert("RGBA")
				file = file.resize((500, 500))
				blend = Image.blend(ci, file, 0.5)
				byt = BytesIO()
				blend.save(byt, format='png')
				byt.seek(0)
				file = discord.File(fp=byt, filename="communism.png")
				return file

			async def async_func():
				thing = functools.partial(sync_func)
				file = await self.bot.loop.run_in_executor(None, thing)
				end = time.perf_counter()
				emed=discord.Embed(title='Blended', color=self.bot.embed_color)
				emed.set_image(url='attachment://communism.png')
				emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')
				await ctx.send(embed=emed, file=file)
			await async_func()

	#some code from https://github.com/daggy1234, edited by me
	@commands.command(help='inserts a user onto a wanted poster')
	async def wanted(self, ctx, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		start = time.perf_counter()
		async with ctx.typing():
			if ctx.message.attachments:
				avimg = BytesIO(await ctx.message.attachments[0].read())
			elif isinstance(image, discord.PartialEmoji):
				avimg = BytesIO(await image.url.read())
			else:
				img = image or ctx.author
				avimg = BytesIO(await img.avatar_url_as(format="jpeg").read())

			def sync_func():
				image = Image.open(avimg)
				ci = image.convert("RGB")
				im = Image.open("assets/wanted.jpeg")
				im = im.convert("RGB")
				tp = ci.resize((800, 800), 0)
				im.paste(tp, (200, 450))
				byt = BytesIO()
				im.save(byt, format='jpeg')
				byt.seek(0)
				file = discord.File(fp=byt, filename="wanted.jpeg")
				return file

			async def async_func():
				thing = functools.partial(sync_func)
				file = await self.bot.loop.run_in_executor(None, thing)
				emed=discord.Embed(title='Arrest them!', color=self.bot.embed_color)
				emed.set_image(url='attachment://wanted.jpeg')
				end = time.perf_counter()
				emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')
				await ctx.send(embed=emed, file=file)
			await async_func()

	#more daggy code, https://github.com/daggy1234
	@commands.command(help='give a medal to youself! you deserve it!')
	async def obama(self, ctx, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		start = time.perf_counter()
		async with ctx.typing():
			if ctx.message.attachments:
				avimg = BytesIO(await ctx.message.attachments[0].read())
			elif isinstance(image, discord.PartialEmoji):
				avimg = BytesIO(await image.url.read())
			else:
				img = image or ctx.author
				avimg = BytesIO(await img.avatar_url_as(format="png").read())

			def sync_func():
				image = Image.open(avimg)
				image = image.convert("RGBA")
				obama_pic = Image.open("assets/obama.png")
				obama_pic = obama_pic.convert("RGBA")
				y = image.resize((300, 300), 1)
				obama_pic.paste(y, (250, 100))
				obama_pic.paste(y, (650, 0))
				byt = BytesIO()
				obama_pic.save(byt, format='png')
				byt.seek(0)
				file = discord.File(fp=byt, filename="obama.png")
				return file

			async def async_func():
				thing = functools.partial(sync_func)
				file = await self.bot.loop.run_in_executor(None, thing)
				emed=discord.Embed(title='Treat yourself nicely!', color=self.bot.embed_color)
				emed.set_image(url='attachment://obama.png')
				end = time.perf_counter()
				emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')
				await ctx.send(embed=emed, file=file)
			await async_func()

	@commands.command(help='nut someone')
	async def nut(self, ctx, image: typing.Union[discord.PartialEmoji, discord.Member]):
		start = time.perf_counter()
		async with ctx.typing():
			if ctx.message.attachments:
				avimg = BytesIO(await ctx.message.attachments[0].read())
			elif isinstance(image, discord.PartialEmoji):
				avimg = BytesIO(await image.url.read())
			else:
				avimg = BytesIO(await image.avatar_url_as(format="png").read())
				img2 = BytesIO(await ctx.author.avatar_url_as(format="png").read())
			def sync_func(img2):
				image = Image.open(avimg)
				image = image.convert("RGBA")
				image = image.resize((45, 45), 1)
				img2 = Image.open(img2)
				img2 = img2.resize((50, 50))
				nuts = Image.open("assets/stretchnuts.png")
				nuts = nuts.convert("RGBA")
				nuts.paste(image, (160, 8))
				nuts.paste(img2, (16, 8))
				byt = BytesIO()
				nuts.save(byt, format='png')
				byt.seek(0)
				file = discord.File(fp=byt, filename="nut.png")
				return file

			async def async_func():
				thing = functools.partial(sync_func, img2)
				file = await self.bot.loop.run_in_executor(None, thing)
				emed=discord.Embed(title='nutted', color=self.bot.embed_color)
				emed.set_image(url='attachment://nut.png')
				end = time.perf_counter()
				emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')
				await ctx.send(embed=emed, file=file)
			await async_func()

	#more daggy code, https://github.com/daggy1234
	@commands.command(help='give a medal to someone when they do something cool')
	async def reward(self, ctx, user: discord.Member, user2: discord.Member=None):
		start = time.perf_counter()
		async with ctx.typing():
			if user2:
				uimg = BytesIO(await user2.avatar_url_as(format='png').read())
			else:
				uimg = BytesIO(await ctx.author.avatar_url_as(format='png').read())
			avimg = BytesIO(await user.avatar_url_as(format="png").read())
			def sync_func(uimg):
				image2 = Image.open(uimg)
				image = Image.open(avimg)
				image = image.convert("RGBA")
				uimg = image2.convert("RGBA")
				obama_pic = Image.open("assets/obama.png")
				obama_pic = obama_pic.convert("RGBA")
				y = image.resize((320, 320), 1)
				uimg = uimg.resize((300, 300), 1)
				obama_pic.paste(y, (275, 95))
				obama_pic.paste(uimg, (650, 0))
				byt = BytesIO()
				obama_pic.save(byt, format='png')
				byt.seek(0)
				file = discord.File(fp=byt, filename="obama.png")
				return file

			async def async_func():
				thing = functools.partial(sync_func, uimg)
				file = await self.bot.loop.run_in_executor(None, thing)
				emed=discord.Embed(title='You deserve this', color=self.bot.embed_color)
				emed.set_image(url='attachment://obama.png')
				end = time.perf_counter()
				emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')
				await ctx.send(embed=emed, file=file)
			await async_func()


	@commands.command(help='Width limit is 1000 and height limit is 500, got that?', hidden=False, brief='Resizes an image.')
	async def resize(self, ctx, width: int, height: int, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		if height < 501 and width < 1001:
			async with ctx.typing():
				if ctx.message.attachments:
					byt = await ctx.message.attachments[0].read()
				elif isinstance(image, discord.PartialEmoji):
					byt = await image.url.read()
				else:
					img = image or ctx.author
					byt = await img.avatar_url_as(format="png").read()
				
				def sync_func():
					im = polaroid.Image(byt)
					im.resize(width, height, 1)
					file = discord.File(BytesIO(im.save_bytes()), filename="stretched.png")
					return file

				async def async_func():
					thing = functools.partial(sync_func)
					file = await self.bot.loop.run_in_executor(None, thing)
					emed=discord.Embed(title='ｒｅｓｉｚｅｄ', color=self.bot.embed_color)
					emed.set_image(url='attachment://stretched.png')
					emed.set_footer(text='Powered by Polaroid')
					await ctx.send(embed=emed, file=file)

				await async_func()
		elif width > 1001:
			await ctx.send('Width can be 1000 pixels wide at max!')
		elif height > 501:
			await ctx.send('Height can be 500 pixels tall at max!')

def setup(bot):
	bot.add_cog(image(bot))