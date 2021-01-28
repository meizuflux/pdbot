from discord.ext import commands
import discord
import os
import aiohttp
import onetimepad
import random
from iso639 import languages
import async_google_trans_new
import datetime
import lyricsgenius
geniustoken = os.environ['genius']
genius = lyricsgenius.Genius(geniustoken)
flipnotetoken = os.environ['tflipnote']
nasakey = os.environ['nasakey']

class fun(commands.Cog):
	"""For the fun commands"""
	def __init__(self, bot):
		self.bot = bot

	

	@commands.command(name='smolpp', hidden=True)
	async def smolpp(self, ctx, *, thing):
		message = thing.capitalize()
		if message == ('You', 'I', 'They'):
			await ctx.send(f'{message} have a smol pp')
		else: 
			await ctx.send(f'{message} has a smol pp')
	
	@commands.command(name='garsh')
	async def garsh(self, ctx):
		await ctx.send('ASTRELLA OUTDATED <:Pog:790609728782073876> CERRET OVERRATED <:Pog:790609728782073876> GARSH ACTIVATED')

	@commands.command(name='copypasta')
	async def copypasta(self, ctx):
		await ctx.send('https://media.discordapp.net/attachments/788422986717200444/790627982813036580/Screenshot_2020-12-21_at_11.10.48_AM.png')
		await ctx.send('https://media.discordapp.net/attachments/788422986717200444/790627978774183936/Screenshot_2020-12-21_at_11.13.03_AM.png')
		await ctx.send('https://media.discordapp.net/attachments/788422986717200444/790627980681543730/Screenshot_2020-12-21_at_11.11.47_AM.png')

	@commands.command(name='astrelladies')
	async def fakeembed(self, ctx):
		embed = discord.Embed(title='he ded', description='can we get an f in the chat')
		embed.colour = 0xFFFFFF  # can be set in 'discord.Embed()' too
		embed.set_image(url='https://media.tenor.com/images/b5e65cd0e7a8c8fef19af759a29d1acd/tenor.gif')

		await ctx.send(embed=embed)

	@commands.command(name='translate', help='Translates text into another language with Google Translate')
	async def gtr(self, ctx, language, *, text: str):
		language = language.capitalize()
		lang = languages.get(name=language)
		g = async_google_trans_new.google_translator()
		gemb = discord.Embed(title='Google Translation', color=0x2F3136)
		gemb.add_field(name='Input:', value=f'```\n{text}\n```')
		gemb.add_field(name=f'Output in {language}:', value=f'```\n{await g.translate(text, lang.alpha2)}\n```', inline=False)
		await ctx.send(embed=gemb)

	@commands.command()
	async def ppsize(self, ctx, user: discord.Member=None):
		if not user:
			user = ctx.author
		size = '='*random.randint(2, 20)
		if user.id == self.bot.author_id:
			size = '='*50
		e = discord.Embed(description=f'8{size}D')
		await ctx.send(embed=e)

	@commands.command(name='blue', help='blue')
	async def blue(self, ctx):
		await ctx.send('https://www.youtube.com/watch?v=HiHPjwyzwNk')

	@commands.command(name='multiply')
	async def multiply(self, ctx, times: int, *, message=None):
		if ctx.author.id != self.bot.owner_id and times > 10:
			await ctx.send('No more than 10 times.')
		else:
			await ctx.send(f'{message} '*times)
		
	@commands.command(name='rascal')
	async def r(self, ctx):
		await ctx.send('I cannot believe it. I can NOT fucking believe it. I simply REFUSE to believe the absolute imcompetent, negligence, of actually not, for ANY of these categories whatsoever, not picking up FUCKING Rascal. This guy doesn\'t get props by anyone, on no one\'s social media radar whatsoever. Everyone\'s talking about like "oh Smurf, ya know, Smurf he\'s-- poor Smurf!" think about Rascal! He literally came into the league at the start of the year, was the BEST Mei. He revolutionized the way you play Echo, and set the guidelines for everyone else in the league for MONTHS! Or pretty much like half the season! And then he comes into the Countdown Cup and plays the Genji, that actually turns the SanFranciscoShockaroundandtheywintheseriesagainstthePhiladelphiaFusion! How is NO ONE, on this PLANET talking about Rascal as one of the most underrated players of the year! It\'s absolutely... HURTING MY SOUL!')

	@commands.command(name='lyrics')
	async def lyric(self, ctx, *, songname):
		cs = aiohttp.ClientSession()
		song = await cs.get('')

	@commands.command(name='chucknorris', aliases=['norris', 'chucknorrisjoke'])
	async def norris(self, ctx):
		data = await self.bot.session.get('https://api.chucknorris.io/jokes/random')
		joke = await data.json()
		e = discord.Embed(title='Chuck Norris Joke', url=joke['url'], description=joke['value'])
		e.set_footer(text=joke['updated_at'])
		e.set_thumbnail(url=joke['icon_url'])
		await ctx.send(embed=e)

	@commands.command(help='Sends a waifu')
	async def waifu(self, ctx, user: discord.Member=None):
		if not user:
			user = ctx.author
		async with self.bot.session.get('https://waifu.pics/api/sfw/waifu') as waifu: # https://waifu.pics/docs DOCS
			waifu = await waifu.json()
			w = discord.Embed(title=f'Waifu for {user.name}')
			w.set_image(url=waifu['url'])
			w.set_footer(text='Powered by waifu.pics')
			await ctx.send(embed=w)

	@commands.command(help='NASA Picture of the day. Optional date arg should be formatted like YYYY-MM-DD')
	async def nasa(self, ctx, dateintime=None):
		try:
			if dateintime is None:
				dateintime = datetime.datetime.utcnow().strftime("%Y-%m-%d")
			async with self.bot.session.get(f'https://api.nasa.gov/planetary/apod?date={dateintime}&api_key={nasakey}') as nasa:
				nasa = await nasa.json()
			nemb = discord.Embed(title=f'NASA Image of the day for {dateintime}', description=nasa['explanation'][:1024])
			try:
				nemb.add_field(name=nasa['title'])
			except TypeError:
				pass
			nemb.set_image(url=nasa['url'])
			try:
				nemb.set_footer(text=f'Copyright: {nasa["copyright"]}')
			except KeyError:
				nemb.set_footer(text='Powered by the NASA APOD API')
			await ctx.send(embed=nemb)
		except KeyError:
			await ctx.send('Enter a valid date please!')

	@commands.command(help='Gets a random cat fact')
	async def catfact(self, ctx):
		async with self.bot.session.get('https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=1') as cat:
			cat = await cat.json()
		async with self.bot.session.get('https://api.thecatapi.com/v1/images/search') as catimg:
			catimg = await catimg.json()
		catemb = discord.Embed(title='Random Cat Fact', description=cat['text'])
		catemb.set_thumbnail(url=catimg[0]['url'])
		catemb.set_footer(text='Powered by the Cat Facts API')
		await ctx.send(embed=catemb)

	@commands.command(help='Gets a random image of a cat')
	async def cat(self, ctx):
		async with self.bot.session.get('https://api.thecatapi.com/v1/images/search') as catimg:
			catimg = await catimg.json()
		catemb = discord.Embed(title='Random Cat')
		catemb.set_image(url=catimg[0]['url'])
		catemb.set_footer(text='Powered by TheCatAPI')
		await ctx.send(embed=catemb)

	@commands.command()
	async def xkcd(self, ctx, query: int = None):
		async with ctx.typing():
			if isinstance(query, int):
				num = query
			else:
				async with self.bot.session.get("https://xkcd.com/info.0.json") as resp:
					max_num = (await resp.json())["num"]
					num = random.randint(1, max_num)

			async with self.bot.session.get(f"https://xkcd.com/{num}/info.0.json") as resp:
				if resp.status in range(400, 500):
					return await ctx.send("Couldn't find a comic with that number.")
				elif resp.status >= 500:
					return await ctx.send("Server error.")
				data = await resp.json()

			embed = discord.Embed(
			title=f"{data['safe_title']} (Number `{data['num']}`)",
			description=data["alt"],
			timestamp=datetime.datetime(year=int(data["year"]), month=int(data["month"]), day=int(data["day"])),
			colour=0x2F3136)
			embed.set_image(url=data["img"])
			embed.set_footer(text="Powered by the XKCD API")
			await ctx.send(embed=embed)

	@commands.command(name='monke', help='reject discord return to monke')
	async def monk(self, ctx, monke: discord.Member=None):
		if not monke:
			monke = ""
		else:
			monke = f"{monke.mention}, "
		await ctx.send(f"https://tenor.com/view/reject-modernity-return-to-monke-monke-gif-19167526\n{monke}return to monke")

	@commands.command(help='Encrypts a message')
	async def encrypt(self, ctx, *, message: str):
		cipher = onetimepad.encrypt(message, 'a_random_key')
		gemb = discord.Embed(title='Encryption', color=0x2F3136)
		gemb.add_field(name='Input:', value=f'```\n{message}\n```')
		gemb.add_field(name='Output:', value=f'```\n{cipher}\n```', inline=False)
		await ctx.send(embed=gemb)
    	

	@commands.command(help='Decrypts a message')
	async def decrypt(self, ctx, *, text: str):
		msg = onetimepad.decrypt(text, 'a_random_key')
		gemb = discord.Embed(title='Decryption', color=0x2F3136)
		gemb.add_field(name='Input:', value=f'```\n{text}\n```')
		gemb.add_field(name='Output:', value=f'```\n{msg}\n```', inline=False)
		await ctx.send(embed=gemb)




def setup(bot):
	bot.add_cog(fun(bot))