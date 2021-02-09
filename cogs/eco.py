from discord.ext import commands
import discord
import utils.embed as qembed
import humanize
import time

class Economy(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot
		self.bot.eco = self.bot.data.economy

	@commands.command(help='Registers you into the database')
	async def register(self, ctx):
		try:
			await self.bot.eco.insert_one({"_id": ctx.author.id, "wallet": 100, "bank": 0})
			await qembed.send(ctx, 'Sucessfully registered you!')
		except:
			await qembed.send(ctx, 'You are already registered!')

	@commands.command(help='View yours or someone elses balance', aliases=['bal'])
	async def balance(self, ctx, user: discord.Member = None):
		try:
			data = await self.bot.eco.find_one({"_id": user.id if user else ctx.author.id})
			e = discord.Embed(title=f'{user.name if user else ctx.author.name}\'s balance', description=f'<:member_join:596576726163914752> **Wallet**: ${humanize.intcomma(data["wallet"])}\n<:member_join:596576726163914752> **Bank**: ${humanize.intcomma(data["bank"])}\n<:member_join:596576726163914752> **Total**: ${humanize.intcomma(data["wallet"] + data["bank"])}', color=self.bot.embed_color, timestamp=ctx.message.created_at)
			e.set_thumbnail(url=user.avatar_url if user else ctx.author.avatar_url)
			await ctx.send(embed=e)
		except TypeError:
			await qembed.send(ctx, f'You need to register! Do `{ctx.prefix}help register` for more info.')
	
	@commands.command(help='Deposits a set amount into your bank', aliases=['dep'])
	async def deposit(self, ctx, amount):
		data = await self.bot.eco.find_one({"_id": ctx.author.id})
		wallet = data["wallet"]
		bank = data["bank"]
		message = 'An error occured'
		if amount.lower() == 'all':
			wallet = 0
			bank = data["bank"] + data["wallet"]
			message = f'You deposited your entire wallet of ${humanize.intcomma(data["wallet"])}'
		else: 
			if int(amount) > data["wallet"]:
				return await qembed.send(ctx, 'You don\'t have that much money in your wallet.')
			if int(amount) < 0:
				return await qembed.send(ctx, 'How exactly are you going to deposit a negative amount of money?')
			else:
				wallet = data["wallet"] - int(amount)
				bank = data["bank"] + int(amount)
				message = f'You deposited ${humanize.intcomma(amount)}'
		await self.bot.eco.replace_one({"_id": ctx.author.id}, {"wallet": wallet, "bank": bank})
		await qembed.send(ctx, message)

	@commands.command(help='Deposits a set amount into your bank', aliases=['wd', 'with'])
	async def withdrawl(self, ctx, amount):
		data = await self.bot.eco.find_one({"_id": ctx.author.id})
		wallet = data["wallet"]
		bank = data["bank"]
		message = 'An error occured'
		if amount.lower() == 'all':
			wallet = data["bank"] + data["wallet"]
			bank = 0
			message = f'You withdrew your entire bank of ${humanize.intcomma(data["bank"])}'
		else: 
			if int(amount) > data["wallet"]:
				return await qembed.send(ctx, 'You don\'t have that much money in your bank.')
			if int(amount) < 0:
				return await qembed.send(ctx, 'You can\'t exactly withdraw a negative amount of money')
			else:
				wallet = data["wallet"] + int(amount)
				bank = data["bank"] - int(amount)
				message = f'You withdrew ${humanize.intcomma(amount)}'
		await self.bot.eco.replace_one({"_id": ctx.author.id}, {"wallet": wallet, "bank": bank})
		await qembed.send(ctx, message)

	@commands.command(help='Lets you send money over to another user', alises=['send'])
	async def transfer(self, ctx, user: discord.Member, amount):
		data = await self.bot.eco.find_one({"_id": ctx.author.id})
		data2 = await self.bot.eco.find_one({"_id": user.id})
		wallet = data["wallet"]
		wallet2 = data2["wallet"]
		message = 'An error occured'
		if amount.lower() == 'all':
			wallet = 0
			wallet2 = data2["wallet"] + data["wallet"]
			message = f'You gave {user.name} your entire wallet of ${humanize.intcomma(data["wallet"])}!'
		else: 
			if int(amount) > data["wallet"]:
				return await qembed.send(ctx, 'You don\'t have that much money in your wallet.')
			if int(amount) < 0:
				return await qembed.send(ctx, f'{ctx.author.name}, it just isn\'t yet possible to send {user.name} a negative amount of money.')
			else:
				wallet = data["wallet"] - int(amount)
				wallet2 = data2["wallet"] + int(amount)
				message = f'You gave {user.name} ${humanize.intcomma(amount)}'
		await self.bot.eco.replace_one({"_id": ctx.author.id}, {"wallet": wallet, "bank": data["bank"]})
		await self.bot.eco.replace_one({"_id": user.id}, {"wallet": wallet2, "bank": data2["bank"]})
		await qembed.send(ctx, message)

def setup(bot):
	bot.add_cog(Economy(bot))