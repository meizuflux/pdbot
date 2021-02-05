import discord
import itertools
import aiohttp
from discord.ext import commands

class MyNewHelp(commands.MinimalHelpCommand):

	def get_opening_note(self):
		return "`<arg>`  means the argument is required\n`[arg]`  means the argument is optional"

	def add_bot_commands_formatting(self, commands, heading):
		if commands:
			joined = '`\u2002•\u2002`'.join(c.name for c in commands)
			self.paginator.add_line('**%s commands:**' % heading)
			self.paginator.add_line(f'`{joined}`')
			self.paginator.add_line()
			


	def get_ending_note(self):
		command_name = self.invoked_with
		return (
			"Type `{0}{1} [command]` for more info on a command.\n"
			"You can also type `{0}{1} [category]` for more info on a category.".format(
				self.clean_prefix, command_name
			)
		)

	async def send_pages(self):
		destination = self.get_destination()
		for page in self.paginator.pages:
			emby = discord.Embed(description=page, color=0x9c5cb4)
			await destination.send(embed=emby)

	async def send_command_help(self, command):
		embed = discord.Embed(title=command.name, color=0x9c5cb4)
		if command.help:
			embed.add_field(name="Help", value=f'```{command.help}```')
		alias = command.aliases
		if alias:
			embed.add_field(name="Aliases", value=f"```{', '.join(alias)}```", inline=False)
		embed.add_field(
            name="Usage", value=f"```{self.get_command_signature(command)}```", inline=False
        )
		embed.set_footer(self.get_ending_note())
		channel = self.get_destination()
		await channel.send(embed=embed)

	async def on_help_command_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			embed = discord.Embed(title="Error", description=str(error))
			await ctx.send(embed=embed)
		if isinstance(error, commands.CommandNotFound):
			embed = discord.Embed(title="Error", description=str(error))
			await ctx.send(embed=embed)
		else:
			raise error

	async def send_bot_help(self, mapping):
		ctx = self.context
		bot = ctx.bot

		if bot.description:
			self.paginator.add_line(bot.description, empty=True)

		note = self.get_opening_note()
		if note:
			self.paginator.add_line(note, empty=True)

		no_category = '\u200b{0.no_category}'.format(self)
		def get_category(command, *, no_category=no_category):
			cog = command.cog
			return cog.qualified_name if cog is not None else no_category

		filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
		to_iterate = itertools.groupby(filtered, key=get_category)

		for category, commands in to_iterate:
			commands = sorted(commands, key=lambda c: c.name) if self.sort_commands else list(commands)
			self.add_bot_commands_formatting(commands, category)

		async with aiohttp.ClientSession() as cs:
			async with cs.get('https://api.github.com/repos/ppotatoo/pdbot/commits/master') as f:
				resp = await f.json()

		if resp["commit"]["message"].capitalize().startswith('Minor'):
			pass
		else:
			self.paginator.add_line('**Latest Github Commit:**')
			self.paginator.add_line(resp["commit"]["message"].capitalize())
			# self.paginator.add_line('you can also choose to write it yourself')
			self.paginator.add_line()

		note = self.get_ending_note()
		if note:
			self.paginator.add_line(note)

		await self.send_pages()