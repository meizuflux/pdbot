import discord
from discord.ext import commands

class MyNewHelp(commands.MinimalHelpCommand):
	async def send_pages(self):
		destination = self.get_destination()
		for page in self.paginator.pages:
			emby = discord.Embed(description=page, color=0x1E90FF)
			await destination.send(embed=emby)

	async def send_command_help(self, command):
		embed = discord.Embed(title=command.name, color=0x1E90FF)
		embed.add_field(name="Help", value=f'```{command.help}```')
		alias = command.aliases
		if alias:
			embed.add_field(name="Aliases", value=f"```{', '.join(alias)}```", inline=False)
		embed.add_field(
            name="Usage", value=f"```{self.get_command_signature(command)}```", inline=False
        )

		channel = self.get_destination()
		await channel.send(embed=embed)