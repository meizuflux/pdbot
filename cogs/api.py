from discord.ext import commands
import discord
import requests
import time
import urllib.parse

class api(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='profile', description='!profile <scoresaberid>')
	async def profile(self, ctx, ssid: int):
		if ssid != int:
			await ctx.send('It looks like you did not enter a number')
		data = requests.get(f'https://new.scoresaber.com/api/player/{ssid}/full').json()
		embed = discord.Embed(title=f"{data['playerInfo']['playerName']}\'s Profile", url=f"https://new.scoresaber.com/u/{ssid}", description=f"Player Ranking: #{data['playerInfo']['rank']} \nCountry Ranking: {data['playerInfo']['country']} #{data['playerInfo']['countryRank']} \nPerformance Points: {data['playerInfo']['pp']}")
		embed.color = 0x2f3136
		embed.set_thumbnail(url=f"https://new.scoresaber.com{data['playerInfo']['avatar']}")
		embed.set_footer(text=f"Sent at {ctx.message.created_at}")
		embed.add_field(name='Score Stats', value=f"Play Count: {data['scoreStats']['totalPlayCount']} \nRanked Play Count: {data['scoreStats']['rankedPlayCount']} \nAverage Ranked Accuracy: {data['scoreStats']['averageRankedAccuracy']:.2f}%", inline=False)
		embed.set_footer(text=f'Powered by the ScoreSaber API')

		await ctx.send(embed=embed)

	@commands.command(name='ssinfo')
	async def info(self, ctx, username: str):
		url = requests.get(f'https://new.scoresaber.com/api/players/by-name/{username}').json()
		ssid = url['players'][0]['playerId']
		data = requests.get(f"https://new.scoresaber.com/api/player/{ssid}/full").json()
		embed = discord.Embed(title=f"{data['playerInfo']['playerName']}\'s Profile", url=f"https://new.scoresaber.com/u/{ssid}", description=f"Player Ranking: #{data['playerInfo']['rank']} \nCountry Ranking: {data['playerInfo']['country']} #{data['playerInfo']['countryRank']} \nPerformance Points: {data['playerInfo']['pp']}")
		embed.color = 0x2f3136
		embed.set_thumbnail(url=f"https://new.scoresaber.com{data['playerInfo']['avatar']}")
		embed.set_footer(text=f"Sent at {ctx.message.created_at}")
		embed.add_field(name='Score Stats', value=f"Play Count: {data['scoreStats']['totalPlayCount']} \nRanked Play Count: {data['scoreStats']['rankedPlayCount']} \nAverage Ranked Accuracy: {data['scoreStats']['averageRankedAccuracy']:.2f}%", inline=False)
		embed.set_footer(text=f'Powered by the ScoreSaber API')

		await ctx.send(embed=embed)

	@commands.command(name='key', description='!key <keyfrombeatsaver> note: older songs do not show duration')
	async def bsr(self, ctx, key: str):
		bad = ['Lawless', 'Lightshow']
		headers = {
    		'User-Agent': 'rank 1 scoresaber 1.0',
				}
		data = requests.get(f'https://beatsaver.com/api/maps/detail/{key}', headers=headers).json()
		cortime = time.strftime('%H:%M:%S', time.gmtime(data['metadata']['duration']))
		embed = discord.Embed(title=data['name'], url=f"https://beatsaver.com/beatmap/{data['key']}")
		embed.color = 0x2f3136
		embed.set_thumbnail(url=f"https://beatsaver.com{data['coverURL']}")
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
		embed.set_footer(text=f'Powered by the BeatSaver API')
		await ctx.send(embed=embed)

	@commands.command(name='ow', help='Currently PC only. Profile must be public.')
	async def ow(self, ctx, region=None, *, BattleTag: str):
		BattleTag = BattleTag.replace('#', '-')
		if len(region) == 0:
			region = 'us'
		data = requests.get(f'https://ow-api.com/v1/stats/pc/{region}/{BattleTag}/profile')
		if data.status_code == 400:
			await ctx.send('Player not found')
		else:
			data = data.json()
			if data['private'] == True:
				await ctx.send(f"Profile is private. They are level {data['prestige']}{data['level']}.")
			else:
				embed = discord.Embed(title=data['name'], url=f'https://www.overbuff.com/players/pc/{BattleTag}?mode=competitive', color=0x2f3136, description=f"Level: {data['prestige']}{data['level']} \nEndorsement Level: {data['endorsement']} \nTotal Games Won: {data['gamesWon']}")
				embed.set_thumbnail(url=data['icon'])
				embed.add_field(name='Competitive Stats', value=f"Tank SR: {data['ratings'][0]['level']}sr \nDamage SR: {data['ratings'][1]['level']}sr \nSupport SR: {data['ratings'][2]['level']}sr")
				embed.set_footer(text=f'Powered by https://ow-api.com')

				await ctx.send(embed=embed)



def setup(bot):
	bot.add_cog(api(bot))