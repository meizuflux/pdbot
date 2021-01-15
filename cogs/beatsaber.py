from discord.ext import commands
import discord
import requests
import urllib.parse
import time
import math
import json
import asyncio
import aiohttp


class BeatSaber(commands.Cog, name='Beat Saber', command_attrs=dict(hidden=False)):
	'''Beat Saber Related Commands'''
	def __init__(self, bot):
		self.bot = bot

	@commands.group(help='Collection of ScoreSaber commands')
	async def ss(self, ctx):
		if ctx.invoked_subcommand is None:
		    await ctx.send_help(str(ctx.command))

	@ss.command(name='info', help='As long as your username doesn\'t contain \'+\'')
	async def info(self, ctx, *, username: str=None):
		if username is None:
			try:
				with open('data.json', 'r') as f:
					data = json.load(f)
					ssid = data['ssinfo'][str(ctx.author.id)]
					message = await ctx.send(f'Getting your stats ...')
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
			await message.edit(content=url['error']['message'])
			
		data = requests.get(f"https://new.scoresaber.com/api/player/{ssid}/full").json()
		await message.edit(content=f'Searching for `{username}` ...\nFormatting `{username}` to use in the URL...\nGetting `{username}\'s` ID from API ...\nGetting `{username}\'s` stats ...')
		grank = math.ceil(int(data['playerInfo']['rank'])/50)
		crank = math.ceil(int(data['playerInfo']['countryRank'])/50)
		embed = discord.Embed(title=f"{data['playerInfo']['playerName']}\'s Profile", url=f"https://new.scoresaber.com/u/{ssid}", description=f"**Player Ranking:** [#{data['playerInfo']['rank']}](https://new.scoresaber.com/rankings/{grank}) \n**Country Ranking:** {data['playerInfo']['country']} [#{data['playerInfo']['countryRank']}](https://scoresaber.com/global/{crank}&country={data['playerInfo']['country']}) \n**Performance Points:** {data['playerInfo']['pp']}")
		embed.color = 0x2f3136
		embed.set_thumbnail(url=f"https://new.scoresaber.com{data['playerInfo']['avatar']}")
		embed.add_field(name='Score Stats', value=f"**Play Count:** {data['scoreStats']['totalPlayCount']} \n**Ranked Play Count:** {data['scoreStats']['rankedPlayCount']} \n**Average Ranked Accuracy:** {data['scoreStats']['averageRankedAccuracy']:.2f}%", inline=False)
		embed.set_footer(text=f'Powered by the ScoreSaber API')
		await message.edit(content=None, embed=embed)

	@ss.command(name='user', help='Ping a user and get their stats')
	async def u(self, ctx, person: discord.Member):
		try:
			with open('data.json', 'r') as f:
						data = json.load(f)
			message = await ctx.send(f'Getting stats for `{person.name}`')
			ssid = data['ssinfo'][str(person.id)]
			data = requests.get(f"https://new.scoresaber.com/api/player/{ssid}/full").json()
			grank = math.ceil(int(data['playerInfo']['rank'])/50)
			crank = math.ceil(int(data['playerInfo']['countryRank'])/50)
			embed = discord.Embed(title=f"{data['playerInfo']['playerName']}\'s Profile", url=f"https://new.scoresaber.com/u/{ssid}", description=f"**Player Ranking:** [#{data['playerInfo']['rank']}](https://new.scoresaber.com/rankings/{grank}) \n**Country Ranking:** {data['playerInfo']['country']} [#{data['playerInfo']['countryRank']}](https://scoresaber.com/global/{crank}&country={data['playerInfo']['country']}) \n**Performance Points:** {data['playerInfo']['pp']}")
			embed.color = 0x2f3136
			embed.set_thumbnail(url=f"https://new.scoresaber.com{data['playerInfo']['avatar']}")
			embed.add_field(name='Score Stats', value=f"**Play Count:** {data['scoreStats']['totalPlayCount']} \n**Ranked Play Count:** {data['scoreStats']['rankedPlayCount']} \n**Average Ranked Accuracy:** {data['scoreStats']['averageRankedAccuracy']:.2f}%", inline=False)
			embed.set_footer(text=f'Powered by the ScoreSaber API')
			await message.edit(content=None, embed=embed)
		except KeyError:
			await ctx.send('The user is not in the database.')

	@ss.command(name='lb', aliases=['top10', 'top'], help='Shows the top 10 players on the leaderboard right now.')
	async def lb(self, ctx):
		message = await ctx.send('Getting the leaderboard from ScoreSaber ...')
		async with aiohttp.ClientSession() as cs:
				async with cs.get('https://new.scoresaber.com/api/players/1') as r:
					lb = await r.json()  # returns dict
		await message.edit(content='Got it! Sending top ten players ...')
		r = discord.Embed(title='Top Ten')
		r.add_field(name=f'#1: {lb["players"][0]["playerName"]}', value=f'Performance Points: {lb["players"][0]["pp"]}\nCountry: {lb["players"][0]["country"]}\nRank Change: +{lb["players"][0]["difference"]}', inline=True)
		r.add_field(name=f'#2: {lb["players"][1]["playerName"]}', value=f'Performance Points: {lb["players"][1]["pp"]}\nCountry: {lb["players"][1]["country"]}\nRank Change: +{lb["players"][1]["difference"]}', inline=True)
		r.add_field(name=f'#3: {lb["players"][2]["playerName"]}', value=f'Performance Points: {lb["players"][2]["pp"]}\nCountry: {lb["players"][2]["country"]}\nRank Change: +{lb["players"][2]["difference"]}', inline=True)
		r.add_field(name=f'#4: {lb["players"][3]["playerName"]}', value=f'Performance Points: {lb["players"][3]["pp"]}\nCountry: {lb["players"][3]["country"]}\nRank Change: +{lb["players"][3]["difference"]}', inline=True)
		r.add_field(name=f'#5: {lb["players"][4]["playerName"]}', value=f'Performance Points: {lb["players"][4]["pp"]}\nCountry: {lb["players"][4]["country"]}\nRank Change: +{lb["players"][4]["difference"]}', inline=True)
		r.add_field(name=f'#6: {lb["players"][5]["playerName"]}', value=f'Performance Points: {lb["players"][5]["pp"]}\nCountry: {lb["players"][5]["country"]}\nRank Change: +{lb["players"][5]["difference"]}', inline=True)
		r.add_field(name=f'#7: {lb["players"][6]["playerName"]}', value=f'Performance Points: {lb["players"][6]["pp"]}\nCountry: {lb["players"][6]["country"]}\nRank Change: +{lb["players"][6]["difference"]}', inline=True)
		r.add_field(name=f'#8: {lb["players"][7]["playerName"]}', value=f'Performance Points: {lb["players"][7]["pp"]}\nCountry: {lb["players"][7]["country"]}\nRank Change: +{lb["players"][7]["difference"]}', inline=True)
		r.add_field(name=f'#9: {lb["players"][8]["playerName"]}', value=f'Performance Points: {lb["players"][8]["pp"]}\nCountry: {lb["players"][8]["country"]}\nRank Change: +{lb["players"][8]["difference"]}', inline=True)
		r.add_field(name=f'#10: {lb["players"][9]["playerName"]}', value=f'Performance Points: {lb["players"][9]["pp"]}\nCountry: {lb["players"][9]["country"]}\nRank Change: +{lb["players"][9]["difference"]}', inline=True)
		r.add_field(name=f'#11: {lb["players"][10]["playerName"]}', value=f'Performance Points: {lb["players"][10]["pp"]}\nCountry: {lb["players"][10]["country"]}\nRank Change: +{lb["players"][10]["difference"]}', inline=True)
		r.add_field(name=f'#12: {lb["players"][11]["playerName"]}', value=f'Performance Points: {lb["players"][11]["pp"]}\nCountry: {lb["players"][11]["country"]}\nRank Change: +{lb["players"][11]["difference"]}', inline=True)
		r.set_footer(text=f'Powered by the ScoreSaber API')
		await message.edit(content=None, embed=r)
		
	@ss.command(name='register', help='Registers you to a ScoreSaber profile')
	async def reg(self, ctx, *, username: str):

		message = await ctx.send(f'Searching for `{username}` ...')
		username = urllib.parse.quote_plus(username.upper())
		username = username.replace('+', '%20')
		await message.edit(content=f'Searching for `{username}` ...\nFormatting `{username}` to use in the URL...')
		url = requests.get(f'https://new.scoresaber.com/api/players/by-name/{username}').json()
		await message.edit(content=f'Searching for `{username}` ...\nFormatting `{username}` to use in the URL...\nGetting `{username}\'s` ID from API ...')
		try:
			ssid = url['players'][0]['playerId']
			data = requests.get(f"https://new.scoresaber.com/api/player/{ssid}/full").json()
			await message.edit(content=f'Searching for `{username}` ...\nFormatting `{username}` to use in the URL...\nGetting `{username}\'s` ID from API ...\nGetting `{username}\'s` stats ...')
			grank = math.ceil(int(data['playerInfo']['rank'])/50)
			crank = math.ceil(int(data['playerInfo']['countryRank'])/50)
			embed = discord.Embed(title=f"Is this you?")
			embed.color = 0x2f3136
			embed.set_thumbnail(url=f"https://new.scoresaber.com{data['playerInfo']['avatar']}")
			embed.add_field(name=data['playerInfo']['playerName'], value=f"**Player Ranking:** [#{data['playerInfo']['rank']}](https://new.scoresaber.com/rankings/{grank}) \n**Country Ranking:** {data['playerInfo']['country']} [#{data['playerInfo']['countryRank']}](https://scoresaber.com/global/{crank}&country={data['playerInfo']['country']}) \n**Performance Points:** {data['playerInfo']['pp']}", inline=False)
			embed.set_footer(text=f'React to this message with ✅ to confirm and ❌ to cancel')
			await message.edit(content=None, embed=embed, delete_after=15)
			await message.add_reaction('✅')
			await message.add_reaction('❌')
			def gcheck(reaction, user):
				return user == ctx.author and str(reaction.emoji) == '✅' or user == ctx.author and str(reaction.emoji) == '❌'
			try:
				reaction, user = await self.bot.wait_for('reaction_add', timeout=14.0, check=gcheck)
			except asyncio.TimeoutError:
				await ctx.send('You did not react in time.')
			else:
				if reaction.emoji == '✅':
					await message.delete()
					with open('data.json', 'r') as f:
						data = json.load(f)
					data['ssinfo'][str(ctx.author.id)] = ssid
					with open('data.json', 'w') as f:
						json.dump(data, f, indent=4)
					await ctx.send(f'Successfully registered ID `{ssid}` with <@{ctx.author.id}>')
				if reaction.emoji == '❌':
					await message.delete()
					await ctx.send('Sorry that I could not help you.')	
		except KeyError:
			await message.edit(content=url['error']['message'])

	@ss.command(name='unregister', help='Unregisters you from a ScoreSaber profile')
	async def ureg(self, ctx):
		e = discord.Embed(description='Would you like to remove yourself from the database?')
		e.set_footer(text=f'React to this message with ✅ to confirm and ❌ to cancel')
		embed = await ctx.send(embed=e, delete_after=15)
		await embed.add_reaction('✅')
		await embed.add_reaction('❌')
		def gcheck(reaction, user):
			return user == ctx.author and str(reaction.emoji) == '✅' or user == ctx.author and str(reaction.emoji) == '❌'
		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=14.0, check=gcheck)
		except asyncio.TimeoutError:
			await ctx.send('You did not react in time.')
		else:
			if reaction.emoji == '✅':
				e = discord.Embed(description=f'Sucessfully removed {ctx.author} and their corresponding ID from the database')
				with open('data.json', 'r') as f:
					data = json.load(f)
					data['ssinfo'].pop(str(ctx.author.id))
				with open('data.json', 'w') as f:
					json.dump(data, f, indent=4)
				await embed.edit(content=None, embed=e)
			if reaction.emoji == '❌':
				e = discord.Embed(description=f'Cancelled unregistering.')
				await embed.edit(content=None, embed=e, delete_after=15)				

	@commands.command(name='key', help='!key <keyfrombeatsaver> note: older songs do not show duration')
	async def bsr(self, ctx, key: str):
		bad = ['Lawless', 'Lightshow']
		headers = {
    		'User-Agent': 'https://github.com/ppotatoo/pdbot, it is a discord bot coded in python',
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

	@commands.command()
	async def typetest(self, ctx, user: discord.Member):
		user = str(user)
		await ctx.send(f'Member\'s ID is `{user.id}')
		if user == str:
			await ctx.send('string')

	@typetest.error
	async def typetest_error(self, ctx, error):
		if isinstance(error, commands.MemberNotFound):
				await ctx.send('I could not find that member...')

	@bsr.error
	async def bsr_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please send a key along with the command.')
		if isinstance(error, commands.CommandInvokeError):
			await ctx.send('Please send a valid key.')
		else:
			raise error


def setup(bot):
	bot.add_cog(BeatSaber(bot))