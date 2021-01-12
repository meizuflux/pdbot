from discord.ext import commands
import discord
import requests
import urllib.parse
import time
import math
import json
import asyncio

class beatsaber(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='ss', help='As long as your username doesn\'t contain \'+\'')
	async def info(self, ctx, *, username: str=None):
		try:
			message = await ctx.send(f'Getting your stats ...')
			with open('data.json', 'r') as f:
				data = json.load(f)
				ssid = data['ssinfo'][str(ctx.author.id)]
		except KeyError:
			await ctx.send('You are not in the database')
		try:
			if username != None:
				message = await ctx.send(f'Searching for `{username}` ...')
				username = urllib.parse.quote_plus(username.upper())
				username = username.replace('+', '%20')
				await message.edit(content=f'Searching for `{username}` ...\nFormatting `{username}` to use in the URL...')
				url = requests.get(f'https://new.scoresaber.com/api/players/by-name/{username}').json()
				await message.edit(content=f'Searching for `{username}` ...\nFormatting `{username}` to use in the URL...\nGetting `{username}\'s` ID from API ...')
				ssid = url['players'][0]['playerId']
		except KeyError:
			await message.edit(content='Player not found.')
		try:		
			data = requests.get(f"https://new.scoresaber.com/api/player/{ssid}/full").json()
			await message.edit(content=f'Searching for `{username}` ...\nFormatting `{username}` to use in the URL...\nGetting `{username}\'s` ID from API ...\nGetting `{username}\'s` stats ...')
			grank = math.ceil(int(data['playerInfo']['rank'])/50)
			crank = math.ceil(int(data['playerInfo']['countryRank'])/50)
			embed = discord.Embed(title=f"{data['playerInfo']['playerName']}\'s Profile", url=f"https://new.scoresaber.com/u/{ssid}", description=f"**Player Ranking:** [#{data['playerInfo']['rank']}](https://new.scoresaber.com/rankings/{grank}) \n**Country Ranking:** {data['playerInfo']['country']} [#{data['playerInfo']['countryRank']}](https://new.scoresaber.com/rankings/{crank}https://scoresaber.com/global/{crank}&country={data['playerInfo']['country']}) \n**Performance Points:** {data['playerInfo']['pp']}")
			embed.color = 0x2f3136
			embed.set_thumbnail(url=f"https://new.scoresaber.com{data['playerInfo']['avatar']}")
			embed.add_field(name='Score Stats', value=f"**Play Count:** {data['scoreStats']['totalPlayCount']} \n**Ranked Play Count:** {data['scoreStats']['rankedPlayCount']} \n**Average Ranked Accuracy:** {data['scoreStats']['averageRankedAccuracy']:.2f}%", inline=False)
			embed.set_footer(text=f'Powered by the ScoreSaber API')
			await message.edit(content=None, embed=embed)



def setup(bot):
	bot.add_cog(beatsaber(bot))