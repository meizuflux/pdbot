from discord.ext import commands
import discord
import requests
import aiohttp
import random



class api(commands.Cog, command_attrs=dict(hidden=False)):
	'''Some random API stuff I'm working on'''
	def __init__(self, bot):
		self.bot = bot

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
				
	@commands.command(name='dankmeme', help='Sends a Dank Meme 😎')
	async def reddit(self, ctx):
		try:
			m = await ctx.send('Getting random dank meme ...')
			async with aiohttp.ClientSession() as cs:
				async with cs.get('https://www.reddit.com/r/dankmemes/hot.json') as r:
					res = await r.json()  # returns dict
					e = discord.Embed(title=res['data']['children'][random.randint(3, 20)]['data']['title'])
					e.set_image(url=res['data']['children'][random.randint(3, 20)]['data']['url_overridden_by_dest'])
					await m.edit(content=None, embed=e)
		except KeyError:
			await ctx.send('Something went wrong.')



def setup(bot):
	bot.add_cog(api(bot))