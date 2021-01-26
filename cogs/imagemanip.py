from discord.ext import commands
import discord
import polaroid
import functools
import typing
import random
from PIL import Image
from PIL import Image as PILImage
from PIL import (ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps,
                 ImageSequence)
from typing import Optional
import os
import aiohttp
from asyncdagpi import Client, ImageFeatures
from io import BytesIO
flipnotetoken = os.environ['tflipnote']
dagpikey = os.environ['dagpikey']

dagpi = Client(dagpikey)

class Image(commands.Cog):
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

	async def alex_image(self, url):
		async with self.bot.session.get(f'https://api.alexflipnote.dev/{url}', headers={'Authorization': flipnotetoken}) as r:
			io = BytesIO(await r.read())
			f = discord.File(fp=io, filename='alex.png')
			return f

	@commands.command(aliases=['didyoumean'], help='"Did you mean" meme. Ex: dym "milk" "with your dad"')
	async def dym(self, ctx, search: str, did_you_mean: str):
		file = await self.alex_image(url=f'didyoumean?top={search}&bottom={did_you_mean}')
		embed = discord.Embed(colour=0x2F3136)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_image(url=f"attachment://alex.png")
		embed.set_footer(text=f"Powered by the AlexFlipnote API")
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
			img = await dagpi.image_process(ImageFeatures.triggered(), url)
			file = discord.File(fp=img.image,filename=f"triggered.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://triggered.gif")
			embed.set_footer(text=f"Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)
			# await self.imgemb(ctx, dfile=file, footername='triggered.gif', powered='the Dagpi API') currently file doesn't send

	@commands.command(aliases=['communism'])
	async def communist(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		async with ctx.typing():
			#if ctx.message.attachments: busted rn
				#url = str(ctx.message.attachments[0].url)
			if isinstance(image, discord.PartialEmoji):
				url = str(image.url)
			else:
				img = image or ctx.author
				url = str(img.avatar_url_as(static_format='png', format='png', size=512))
			img = await dagpi.image_process(ImageFeatures.communism(), url)
			file = discord.File(fp=img.image,filename=f"communism.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://communism.gif")
			embed.set_footer(text=f"Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)	

	@commands.command()
	async def wanted(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		async with ctx.typing():
			#if ctx.message.attachments: busted rn
				#url = str(ctx.message.attachments[0].url)
			if isinstance(image, discord.PartialEmoji):
				url = str(image.url)
			else:
				img = image or ctx.author
				url = str(img.avatar_url_as(static_format='png', format='png', size=512))
			img = await dagpi.image_process(ImageFeatures.wanted(), url)
			file = discord.File(fp=img.image,filename=f"wanted.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://wanted.png")
			embed.set_footer(text=f"Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)

	@commands.command()
	async def obama(self, ctx, *, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		async with ctx.typing():
			#if ctx.message.attachments: busted rn
				#url = str(ctx.message.attachments[0].url)
			if isinstance(image, discord.PartialEmoji):
				url = str(image.url)
			else:
				img = image or ctx.author
				url = str(img.avatar_url_as(static_format='png', format='png', size=512))
			img = await dagpi.image_process(ImageFeatures.obama(), url)
			file = discord.File(fp=img.image,filename=f"obama.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://obama.png")
			embed.set_footer(text=f"Powered by the Dagpi API")
			await ctx.send(embed=embed, file=file)

	@commands.command()
	async def twitter(self, ctx, user: discord.Member, *, text: str):
		async with ctx.typing():
			url = str(user.avatar_url_as(static_format='png', format='png', size=512))
			disname = user.display_name
			name = disname.replace(' ', '')
			img = await dagpi.image_process(ImageFeatures.tweet(), text=text, url=url, username=name)
			file = discord.File(fp=img.image,filename=f"tweet.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://tweet.png")
			embed.set_footer(text=f"Powered by the Dagpi API")
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
			img = await dagpi.image_process(ImageFeatures.five_guys_one_girl(), url=url, url2=url2)
			file = discord.File(fp=img.image,filename=f"five_guys_one_girl.{img.format}")
			embed = discord.Embed(colour=0x2F3136)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_image(url=f"attachment://five_guys_one_girl.png")
			embed.set_footer(text=f"Powered by the Dagpi API")
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

	@commands.command(help='me learning how to use executors', hidden=False)
	async def resize(self, ctx, width: int=None, height: int=None, image: typing.Union[discord.PartialEmoji, discord.Member] = None):
		async with ctx.typing():
			byt = await ctx.author.avatar_url_as(format="png").read()
			
			def sync_func():
				im = polaroid.Image(byt)
				im.resize(width, height, 1)
				file = discord.File(BytesIO(im.save_bytes()), filename=f"stretched.png")
				return file

			async def async_func():
				thing = functools.partial(sync_func)
				file = await self.bot.loop.run_in_executor(None, thing)
				await ctx.send('ｒｅｓｉｚｅｄ', file=file)

			await async_func()



def setup(bot):
	bot.add_cog(Image(bot))