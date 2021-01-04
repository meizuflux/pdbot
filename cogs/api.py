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
		
		embed = discord.Embed(title=f"{data['playerInfo']['playerName']}\'s Profile", url=f"https://new.scoresaber.com/u/{args}", description=f"Player Ranking: #{data['playerInfo']['rank']} \nCountry Ranking: {data['playerInfo']['country']} #{data['playerInfo']['countryRank']} \nPerformance Points: {data['playerInfo']['pp']}")
		embed.color = 0x2f3136
		embed.set_thumbnail(url=f"https://new.scoresaber.com{data['playerInfo']['avatar']}")
		embed.set_footer(text=f"Sent at {ctx.message.created_at}")
		embed.add_field(name='Score Stats', value=f"Play Count: {data['scoreStats']['totalPlayCount']} \nRanked Play Count: {data['scoreStats']['rankedPlayCount']} \nAverage Ranked Accuracy: {data['scoreStats']['averageRankedAccuracy']}%", inline=False)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_footer(text=f'Powered by the ScoreSaber API')

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(api(bot))