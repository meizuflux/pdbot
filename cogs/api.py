from discord.ext import commands
import discord
import requests
import time
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
		embed.add_field(name='Score Stats', value=f"Play Count: {data['scoreStats']['totalPlayCount']} \nRanked Play Count: {data['scoreStats']['rankedPlayCount']} \nAverage Ranked Accuracy: {data['scoreStats']['averageRankedAccuracy']:.2f}%", inline=False)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_footer(text=f'Powered by the ScoreSaber API')

		await ctx.send(embed=embed)

	@commands.command(name='key', description='!key <keyfrombeatsaver> note: older songs do not show duration')
	async def key(self, ctx, args):
		bad = ['Lawless', 'Lightshow']
		headers = {
    		'User-Agent': 'rank 1 scoresaber 1.0',
				}
		data = requests.get(f'https://beatsaver.com/api/maps/detail/{args}', headers=headers).json()
		cortime = time.strftime('%H:%M:%S', time.gmtime(data['metadata']['duration']))
		embed = discord.Embed(title=data['name'], url=f"https://beatsaver.com/beatmap/{data['key']}")
		embed.color = 0x2f3136
		embed.set_thumbnail(url=f"https://beatsaver.com{data['coverURL']}")
		#if data['metadata']['songSubName'] == "":
			#pass
		#else:
			#embed.add_field(name=f"Song Sub Name", value=f"{data['metadata']['songSubName']}", inline=True)
		embed.add_field(name=f"Author", value=f"{data['metadata']['songAuthorName']}", inline=False)
		embed.add_field(name=f"Mapper", value=f"{data['metadata']['levelAuthorName']}", inline=False)
		embed.add_field(name=f"Uploader", value=f"{data['uploader']['username']}", inline=True)
		embed.add_field(name=f"Key", value=f"{data['key']}", inline=False)
		if data['metadata']['duration'] != 0:
			embed.add_field(name=f"Duration", value=f"{cortime}")
		bad = ['Lawless', 'Lightshow']
		charac = data['metadata']['characteristics'][0]['name']
		if charac in bad:
			embed.add_field(name=f"Playable on Quest?", value=f"No", inline=False)
		else:
			embed.add_field(name=f"Playable on Quest?", value=f"Yes", inline=False)
		embed.add_field(name=f"BPM", value=f"{data['metadata']['bpm']}", inline=False)
		embed.add_field(name=f"Download Link", value=f"https://beatsaver.com/api/download/key/{data['key']}", inline=False)
		embed.add_field(name=f"OneClick Install", value=f"beatsaver://{data['key']}", inline=True)
		embed.add_field(name=f"Preview", value=f"https://skystudioapps.com/bs-viewer/?id={data['key']}", inline=False)
		await ctx.send(embed=embed)



def setup(bot):
	bot.add_cog(api(bot))