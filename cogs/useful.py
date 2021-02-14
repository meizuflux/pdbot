import discord
import itertools
import aiohttp
import contextlib
import psutil
import platform
import pathlib
from pkg_resources import get_distribution
import humanize
import re
from utils.default import plural, CantRun
from discord.ext import commands



class Help(commands.MinimalHelpCommand):
    def get_command_signature(self, command, ctx=None):
        """Method to return a commands name and signature"""
        if not ctx:
            if not command.signature and not command.parent:
                return f'`{self.clean_prefix}{command.name}`'
            if command.signature and not command.parent:
                return f'`{self.clean_prefix}{command.name}` `{command.signature}`'
            if not command.signature and command.parent:
                return f'`{self.clean_prefix}{command.parent}` `{command.name}`'
            else:
                return f'`{self.clean_prefix}{command.parent}` `{command.name}` `{command.signature}`'
        else:
            def get_invoke_with():
                msg = ctx.message.content
                escape = "\\"
                prefixmax = re.match(f'{escape}{escape.join(ctx.prefix)}', msg).regs[0][1]
                return msg[prefixmax:msg.rindex(ctx.invoked_with)]

            if not command.signature and not command.parent:
                return f'{ctx.prefix}{ctx.invoked_with}'
            if command.signature and not command.parent:
                return f'{ctx.prefix}{ctx.invoked_with} {command.signature}'
            if not command.signature and command.parent:
                return f'{ctx.prefix}{get_invoke_with()}{ctx.invoked_with}'
            else:
                return f'{ctx.prefix}{get_invoke_with()}{ctx.invoked_with} {command.signature}'

    async def send_error_message(self, error):
    	ctx = self.context
    	destination = self.get_destination()
    	embed=discord.Embed(description=error, color=0x9c5cb4, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    	await destination.send(embed=embed)

    def command_not_found(self, string):
    	return 'No command called "{}" found.'.format(string)

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
    		"Type {0}{1} [command] for more info on a command.\n"
			"You can also type {0}{1} [category] for more info on a category.".format(
				self.clean_prefix, command_name
			)
		)

    async def send_pages(self):
        ctx = self.context
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=0x9c5cb4, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await destination.send(embed=emby)
	
    def add_subcommand_formatting(self, command):
    	fmt = '{0} \N{EN DASH} {1}' if command.short_doc else '{0} \N{EN DASH} This command is not documented'
    	self.paginator.add_line(fmt.format(self.get_command_signature(command), command.short_doc))

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
            self.paginator.add_line(bot.description, empty=False)

        no_category = '\u200b{0.no_category}'.format(self)
        def get_category(command, *, no_category=no_category):
            cog = command.cog
            return cog.qualified_name if cog is not None else no_category

        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
        to_iterate = itertools.groupby(filtered, key=get_category)

        for category, commands in to_iterate:
            commands = sorted(commands, key=lambda c: c.name) if self.sort_commands else list(f'**{commands}**')
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
            
        self.paginator.add_line(self.get_ending_note())

        await self.send_pages()

    def get_help(self, command, brief=True):
        real_help = command.help or "This command is not documented."
        return real_help if not brief else command.short_doc or real_help

    async def send_cog_help(self, cog):
        bot = self.context.bot
        if bot.description:
            self.paginator.add_line(bot.description)

        note = self.get_opening_note()
        if note:
            self.paginator.add_line(note, empty=True)

        filtered = await self.filter_commands(cog.get_commands(), sort=self.sort_commands)
        if filtered:
            self.paginator.add_line('**%s %s**' % (cog.qualified_name, self.commands_heading))
            if cog.description:
                self.paginator.add_line(cog.description, empty=True)
            for command in filtered:
                self.add_subcommand_formatting(command)

        await self.send_pages()

    def get_command_help(self, command):
        ctx = self.context
        embed = discord.Embed(title=self.get_command_signature(command), description=f'```{self.get_help(command, brief=False)}```', color=0x9c5cb4, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=f"```{', '.join(alias)}```", inline=False)
        if isinstance(command, commands.Group):
            subcommand = command.commands
            value = "\n".join(f'{self.get_command_signature(c)} \N{EN DASH} {c.short_doc}' for c in subcommand)
            embed.add_field(name=plural("Subcommand(s)", len(subcommand)), value=value)

        return embed

    async def handle_help(self, command):
        with contextlib.suppress(commands.CommandError):
            await command.can_run(self.context)
            return await self.context.reply(embed=self.get_command_help(command), mention_author=False)
        raise CantRun("You don't have enough permissions to see this help.") from None

    async def send_group_help(self, group):
        await self.handle_help(group)

    async def send_command_help(self, command):
        await self.handle_help(command)

class Useful(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot
		self._original_help_command = bot.help_command
		bot.help_command = Help(command_attrs=dict(hidden=True))
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self._original_help_command

	@commands.command(aliases=['information', 'botinfo'],
	help='Gets info about the bot')
	async def info(self, ctx):
		msg = await ctx.send('Getting bot information ...')
		avgmembers = sum([guild.member_count
		for guild in self.bot.guilds]) / len(self.bot.guilds)
		cpuUsage = psutil.cpu_percent()
		cpuFreq = psutil.cpu_freq().current
		ramusage = humanize.naturalsize(
		psutil.Process().memory_full_info().pss)

		pyVersion = platform.python_version()
		libVersion = get_distribution("discord.py").version
		hosting = platform.platform()

		p = pathlib.Path('./')
		ls = fc = 0
		for f in p.rglob('*.py'):
			if str(f).startswith("venv"):
				continue
			fc += 1
			with f.open() as of:
				for l in of.readlines():
					ls += 1

		emb = discord.Embed(description=self.bot.description, colour=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		emb.set_author(name=self.bot.user.name,
		url='https://github.com/ppotatoo/pdbot',
		icon_url=self.bot.user.avatar_url)
		emb.add_field(name='Developer',
		value=f'```ppotatoo#9688 ({self.bot.author_id})```',
		inline=False)
		emb.add_field(name='<:online:801444524148523088> Uptime',value=f'[Check Bot Status](https://stats.uptimerobot.com/Gzv84sJ9oV \"UptimeRobot\")\n```{humanize.precisedelta(self.bot.start_time, format="%0.0f")}```',inline=False)
		emb.add_field(name='Hosting', value=f'```{hosting}```', inline=False)

		emb.add_field(name='CPU Usage', value=f'```{cpuUsage:.2f}%```', inline=True)
		emb.add_field(name='CPU Frequency', value=f'```{cpuFreq} MHZ```', inline=True)
		emb.add_field(name='Memory Usage', value=f'```{ramusage}```', inline=True)
		emb.add_field(name='<:python:801444523623710742> Python Version', value=f'```{pyVersion}```', inline=True)
		emb.add_field(name='<:discordpy:801444523854135307> Discord.py Version', value=f'```{libVersion}```', inline=True)

		emb.add_field(name='Line Count', value=f'```{ls:,} lines```', inline=False)
		emb.add_field(name='Command Count', value=f'```{len(set(self.bot.walk_commands()))-31} commands```',inline=True)
		emb.add_field(name='Command Use:',value=f'```{self.bot.counter-1} commands since reboot```',inline=True)
		emb.add_field(name='Guild Count',value=f'```{str(len(self.bot.guilds))} guilds```',inline=False)

		emb.add_field(name='Member Count',value=f'```{str(sum([guild.member_count for guild in self.bot.guilds]))} members```',inline=True)
		emb.add_field(name='Average Member Count',value=f'```{avgmembers:.0f} members per guild```')
		await msg.edit(content=None, embed=emb)


def setup(bot):
	bot.add_cog(Useful(bot))