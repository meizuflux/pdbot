import discord
from discord.ext import commands

class MyNewHelp(commands.MinimalHelpCommand):

	def get_opening_note(self):
		return "<> means the argument is required\n[] means the argument is optional"

	def add_bot_commands_formatting(self, commands, heading):
		if commands:
			joined = '`\u2002•\u2002`'.join(c.name for c in commands)
			self.paginator.add_line('**%s**' % heading)
			self.paginator.add_line(f'`{joined}`')
			self.paginator.add_line('')

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
