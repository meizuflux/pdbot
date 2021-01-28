from discord.ext import commands
import discord
import polaroid
import functools
import typing
import os
import time
from PIL import Image
from asyncdagpi import ImageFeatures
from io import BytesIO
flipnotetoken = os.environ['tflipnote']

class image(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@staticmethod
	async def imgemb(ctx, dfile: discord.File, footername, powered):
		embed = discord.Embed(colour=0x2F3136)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_image(url=f"attachment://{footername}")
		embed.set_footer(text=f"Powered by {powered}")
		await ctx.send(embed=embed, file=dfile)

	@staticmethod
	async def manip(ctx, image, *, method: str, method_args: list = None, text: str = None):
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
			if method_args is None:
			        method_args = []
			method = getattr(img, method)
			method(*method_args)
			file = discord.File(BytesIO(img.save_bytes()), filename="polaroid.png")
			end = time.perf_counter()
			embed = discord.Embed(description=text, colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://polaroid.png")
			embed.set_footer(text=f"Backend finished in {end-start:.2f} seconds")
			await ctx.send(embed=embed, file=file)

	async def alex_image(self, url):
		async with self.bot.session.get(f'https://api.alexflipnote.dev/{url}', headers={'Authorization': flipnotetoken}) as r:
			io = BytesIO(await r.read())
			f = discord.File(fp=io, filename='alex.png')
			return f
		
	@commands.command()
	async def comm(self, ctx):
		async with self.bot.session.get(f'https://api.alexflipnote.dev/filter/communist?{ctx.author.avatar_url}', headers={'Authorization': flipnotetoken}) as r:
			io = BytesIO(await r.read())
			f = discord.File(fp=io, filename='alex.png')
			await ctx.send(file=f)

	@commands.command(aliases=['didyoumean'], help='"Did you mean" meme. Ex: dym "milk" "with your dad"')
	async def dym(self, ctx, search: str, did_you_mean: str):
		file = await self.alex_image(url=f'didyoumean?top={search}&bottom={did_you_mean}')
		embed = discord.Embed(colour=0x2F3136)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_image(url="attachment://alex.png")
		embed.set_footer(text="Powered by the AlexFlipnote API")
		await ctx.send(embed=embed, file=file)

	@commands.command(aliases=['trigger'])
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
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://triggered.gif")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)
			# await self.imgemb(ctx, dfile=file, footername='triggered.gif', powered='the Dagpi API') currently file doesn't send

	@commands.command(aliases=['communism'])
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
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://communism.gif")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)	

	@commands.command()
	async def slowwanted(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		async with ctx.typing():
			#if ctx.message.attachments: busted rn
				#url = str(ctx.message.attachments[0].url)
			if isinstance(image, discord.PartialEmoji):
				url = str(image.url)
			else:
				img = image or ctx.author
				url = str(img.avatar_url_as(static_format='png', format='png', size=512))
			img = await self.bot.dagpi.image_process(ImageFeatures.wanted(), url)
			file = discord.File(fp=img.image,filename=f"wanted.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://wanted.png")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)

	@commands.command()
	async def slowobama(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		async with ctx.typing():
			#if ctx.message.attachments: busted rn
				#url = str(ctx.message.attachments[0].url)
			if isinstance(image, discord.PartialEmoji):
				url = str(image.url)
			else:
				img = image or ctx.author
				url = str(img.avatar_url_as(static_format='png', format='png', size=512))
			img = await self.bot.dagpi.image_process(ImageFeatures.obama(), url)
			file = discord.File(fp=img.image,filename=f"obama.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://obama.png")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)

	@commands.command()
	async def twitter(self, ctx, user: discord.Member, *, text: str):
		async with ctx.typing():
			url = str(user.avatar_url_as(static_format='png', format='png', size=512))
			disname = user.display_name
			name = disname.replace(' ', '')
			img = await self.bot.dagpi.image_process(ImageFeatures.tweet(), text=text, url=url, username=name)
			file = discord.File(fp=img.image,filename=f"tweet.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://tweet.png")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)
			
	@commands.command(name='5g1g')
	async def fgog(self, ctx, user1: discord.Member, user2: discord.Member):
		async with ctx.typing():
			#if ctx.message.attachments: busted rn
				#url = str(ctx.message.attachments[0].url)
			#if isinstance(image, discord.PartialEmoji):
				#url = str(image.url)
			url = str(user1.avatar_url_as(static_format='png', format='png', size=512))
			url2 = str(user2.avatar_url_as(static_format='png', format='png', size=512))
			img = await self.bot.dagpi.image_process(ImageFeatures.five_guys_one_girl(), url=url, url2=url2)
			file = discord.File(fp=img.image,filename=f"five_guys_one_girl.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url="attachment://five_guys_one_girl.png")
			embed.set_footer(text="Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)

	@commands.command(help='Makes an image rainbowey')
	async def rainbow(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='apply_gradient')

	@commands.command(help='like putin')
	async def wide(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='resize', method_args=(2000, 900, 1), text='ｗｉｄｅ')

	@commands.command(help='Inverts an image')
	async def invert(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='invert')

	@commands.command(help='It\'s like looking in a mirror')
	async def flip(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='fliph')

	@commands.command(help='Blurs an image? Duh')
	async def blur(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='box_blur')

	@commands.command(help='cursed')
	async def sobelh(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='sobel_horizontal')

	@commands.command(help='cursed')
	async def sobelv(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='sobel_vertical')

	@commands.command(help='Decomposes the image')
	async def decompose(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='decompose_max')

	@commands.command(help='Turns an image black and white')
	async def grayscale(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='grayscale')
		
	@commands.command(help='Solarizes an image')
	async def solarize(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='solarize')
		
	@commands.command(help='Rotates an image sideways')
	async def sideways(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='rotate90')

	@commands.command(help='Rotates an image upsidedown', example='upsidedown person')
	async def upsidedown(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		await self.manip(ctx, image, method='rotate180')



	@commands.command(help='makes an image communist')
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
				emed=discord.Embed(title='Communism', color=0x2F3136)
				emed.set_image(url='attachment://communism.png')
				emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')
				await ctx.send(embed=emed, file=file)
			await async_func()

	#some code from https://github.com/daggy1234, edited by me
	@commands.command(help='makes an image wanted')
	async def wanted(self, ctx, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
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
				ci = image.convert("RGBA")
				im = Image.open("assets/wanted.png")
				im = im.convert("RGBA")
				tp = ci.resize((800, 800), 0)
				im.paste(tp, (200, 450))
				byt = BytesIO()
				im.save(byt, format='png')
				byt.seek(0)
				file = discord.File(fp=byt, filename="communism.png")
				return file

			async def async_func():
				thing = functools.partial(sync_func)
				file = await self.bot.loop.run_in_executor(None, thing)
				emed=discord.Embed(title='Arrest them!', color=0x2F3136)
				emed.set_image(url='attachment://communism.png')
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
				ci = image.convert("RGBA")
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
				emed=discord.Embed(title='Treat yourself nicely!', color=0x2F3136)
				emed.set_image(url='attachment://obama.png')
				end = time.perf_counter()
				emed.set_footer(text=f'Backend finished in {end-start:.2f} seconds')
				await ctx.send(embed=emed, file=file)
			await async_func()


	@commands.command(help='Width limit is 1000 and height limit is 500, got that?', hidden=False)
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
					emed=discord.Embed(title='ｒｅｓｉｚｅｄ', color=0x2F3136)
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