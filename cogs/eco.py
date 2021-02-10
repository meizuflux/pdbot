from discord.ext import commands
import discord
import utils.embed as qembed
import humanize
import time
import typing

class Economy(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot
		self.bot.eco = self.bot.data.economy

	@staticmethod
	async def get_stats(self, id: int):
		try:
			data = await self.bot.eco.find_one({"_id": id})
			wallet = data["wallet"]
			bank = data["bank"]
		except:
			await self.bot.eco.insert_one({"_id": id, "wallet": 100, "bank": 0})
			data = await self.bot.eco.find_one({"_id": id})
			wallet = data["wallet"]
			bank = data["bank"]
		return wallet, bank

	@commands.command(help='Registers you into the database')
	async def register(self, ctx):
		try:
			await self.bot.eco.insert_one({"_id": ctx.author.id, "wallet": 100, "bank": 0})
			await qembed.send(ctx, 'Sucessfully registered you!')
		except:
			await qembed.send(ctx, 'You are already registered!')

	@commands.command(help='View yours or someone elses balance', aliases=['bal'])
	async def balance(self, ctx, user: discord.Member = None):
		data = await self.get_stats(self, user.id if user else ctx.author.id)
		wallet = data[0]
		bank = data[1]
		e = discord.Embed(title=f'{user.name if user else ctx.author.name}\'s balance', description=f'<:member_join:596576726163914752> **Wallet**: ${humanize.intcomma(wallet)}\n<:member_join:596576726163914752> **Bank**: ${humanize.intcomma(bank)}\n<:member_join:596576726163914752> **Total**: ${humanize.intcomma(wallet + bank)}', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		e.set_thumbnail(url=user.avatar_url if user else ctx.author.avatar_url)
		await ctx.send(embed=e)
	
	@commands.command(help='Deposits a set amount into your bank', aliases=['dep'])
	async def deposit(self, ctx, amount):
		data = await self.get_stats(self, ctx.author.id)
		wallet = data[0]
		bank = data[1]
		message = 'An error occured'
		if amount.lower() == 'all':
			wallet = 0
			bank = bank + wallet
			message = f'You deposited your entire wallet of ${humanize.intcomma(wallet)}'
		else: 
			if int(amount) > wallet:
				return await qembed.send(ctx, 'You don\'t have that much money in your wallet.')
			if int(amount) < 0:
				return await qembed.send(ctx, 'How exactly are you going to deposit a negative amount of money?')
			else:
				wallet = wallet - int(amount)
				bank = bank + int(amount)
				message = f'You deposited ${humanize.intcomma(amount)}'
		await self.bot.eco.replace_one({"_id": ctx.author.id}, {"wallet": wallet, "bank": bank})
		await qembed.send(ctx, message)

	@commands.command(help='Deposits a set amount into your bank', aliases=['wd', 'with', 'withdraw'])
	async def withdrawl(self, ctx, amount):
		data = await self.get_stats(self, ctx.author.id)
		wallet = data[0]
		bank = data[1]
		message = 'An error occured'
		if amount.lower() == 'all':
			wallet = bank + wallet
			bank = 0
			message = f'You withdrew your entire bank of ${humanize.intcomma(bank)}'
		else: 
			if int(amount) > bank:
				return await qembed.send(ctx, 'You don\'t have that much money in your bank.')
			if int(amount) < 0:
				return await qembed.send(ctx, 'You can\'t exactly withdraw a negative amount of money')
			if bank < int(amount):
				return await qembed.send(ctx, 'You don\'t have that much money!')
			else:
				wallet = wallet + int(amount)
				bank = bank - int(amount)
				message = f'You withdrew ${humanize.intcomma(amount)}'
		await self.bot.eco.replace_one({"_id": ctx.author.id}, {"wallet": wallet, "bank": bank})
		await qembed.send(ctx, message)

	@commands.command(help='Lets you send money over to another user', alises=['send'])
	async def transfer(self, ctx, user: discord.Member, amount: typing.Union[str, int]):
		#data = self.get_stats()
		data = await self.get_stats(self, ctx.author.id)
		author_wallet = data[0]
		author_bank = data[1]

		data2 = await self.get_stats(self, user.id)
		target_wallet = data2[0]
		target_bank = data2[1]

		if isinstance(amount, int): 
			if amount > author_wallet:
				return await qembed.send(ctx, 'You don\'t have that much money in your wallet.')
			elif amount <= 0:
				return await qembed.send(ctx, f'{ctx.author.name}, it just isn\'t yet possible to send {user.name} a negative amount of money.')
			amount = int(amount)
		elif isinstance(amount, str) and amount.lower() == 'all':
			amount = author_wallet 

		author_wallet -= int(amount)
		target_wallet += int(amount)     

		await self.bot.eco.replace_one({"_id": ctx.author.id}, {"wallet": author_wallet, "bank": author_bank})
		await self.bot.eco.replace_one({"_id": user.id}, {"wallet": target_wallet, "bank": target_bank})

		await qembed.send(ctx, f'You gave {user.name} ${humanize.intcomma(amount)}')

def setup(bot):
	bot.add_cog(Economy(bot))