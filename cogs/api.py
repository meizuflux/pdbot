from discord.ext import commands
import discord
import requests
import json

class api(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='profile', description='!profile <scoresaberid>')
	async def profile(self, ctx, args):
		#if args.isdidget() == False:
			#await ctx.send('It looks like you did not enter a number')
		data = requests.get(f'https://new.scoresaber.com/api/player/{args}/full').json()
		
		embed = discord.Embed(title='Command Use')
		embed.color = 0x2f3136
		embed.set_thumbnail(url=f"https://new.scoresaber.com{data['playerInfo']['avatar']}")
		embed.set_footer(text=f"Sent at {ctx.message.created_at}")
		embed.add_field(name=data['playerInfo']['playerName'], value=f"PP: {data['playerInfo']['pp']} \nRank: #{data['playerInfo']['rank']} \nCountry Rank: {data['playerInfo']['country']} #{data['playerInfo']['countryRank']}", inline=False)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_footer(text=f'Powered by the ScoreSaber API')

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(api(bot))