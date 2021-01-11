from discord.ext import commands
import discord
import os
import urllib.parse
from utils import argparser
flipnotetoken = os.environ['tflipnote']

class fun(commands.Cog):
	"""For the fun commands"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='smolpp', hidden=True)
	async def smolpp(self, ctx, *, message):
		message = message.capitalize()
		if message == 'You' or message == 'I':
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
		embed.set_image(url='https://media.discordapp.net/attachments/786309313786019891/790598215137099807/tenor_2.gif')

		await ctx.send(embed=embed)

	@commands.command(name='blue', help='blue')
	async def blue(self, ctx):
		await ctx.send('https://www.youtube.com/watch?v=HiHPjwyzwNk')

	@commands.command(name='multiply')
	async def multiply(self, ctx, times: int, *, message=None):
		await ctx.send(f'{message} '*times)
		
	@commands.command(name='rascal')
	async def r(self, ctx):
		await ctx.send('I cannot believe it. I can NOT fucking believe it. I simply REFUSE to believe the absolute imcompetent, negligence, of actually not, for ANY of these categories whatsoever, not picking up FUCKING Rascal. This guy doesn\'t get props by anyone, on no one\'s social media radar whatsoever. Everyone\'s talking about like "oh Smurf, ya know, Smurf he\'s-- poor Smurf!" think about Rascal! He literally came into the league at the start of the year, was the BEST Mei. He revolutionized the way you play Echo, and set the guidelines for everyone else in the league for MONTHS! Or pretty much like half the season! And then he comes into the Countdown Cup and plays the Genji, that actually turns the SanFranciscoShockaroundandtheywintheseriesagainstthePhiladelphiaFusion! How is NO ONE, on this PLANET talking about Rascal as one of the most underrated players of the year! It\'s absolutely... HURTING MY SOUL!')

	@commands.command()
	async def supreme(self, ctx, *, text: commands.clean_content(fix_channel_mentions=True)):
		""" Make a fake Supreme logo
        Arguments:
            --dark | Make the background to dark colour
            --light | Make background to light and text to dark colour
        """
		parser = argparser.Arguments()
		parser.add_argument('input', nargs="+", default=None)
		parser.add_argument('-d', '--dark', action='store_true')
		parser.add_argument('-l', '--light', action='store_true')

		args, valid_check = parser.parse_args(text)
		if not valid_check:
		    return await ctx.send(args)

		inputText = urllib.parse.quote(' '.join(args.input))
		if len(inputText) > 500:
		    return await ctx.send(f"**{ctx.author.name}**, the Supreme API is \\limited to 500 characters, sorry.")

		darkorlight = ""
		if args.dark:
		    darkorlight = "dark=true"
		if args.light:
		    darkorlight = "light=true"
		if args.dark and args.light:
		    return await ctx.send(f"**{ctx.author.name}**, you can't define both --dark and --light, sorry..")

		await self.api_img_creator(ctx, f"https://api.alexflipnote.dev/supreme?text={inputText}&{darkorlight}", "supreme.png", token=flipnotetoken)

	

	

def setup(bot):
	bot.add_cog(fun(bot))