import discord
import itertools
import aiohttp
import contextlib
import inspect
import json
import re
from utils.default import plural
from discord.ext import commands
import utils.embed as qembed

class CantRun(commands.CommandError):
    def __init__(self, message, *arg):
        super().__init__(message=message, *arg)


class MyNewHelp(commands.MinimalHelpCommand):

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
        destination = self.get_destination()
        note = self.get_ending_note()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=0x9c5cb4,).set_footer(text=note)
            await destination.send(embed=emby)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f'`{self.get_command_signature(command)}`', color=0x9c5cb4)
        he = command.help if command.help else 'No help provided, suck it up'
        embed.add_field(name="Help", value=f'```{he}```')
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=f"```{', '.join(alias)}```", inline=False)
        #embed.add_field(
            #name="Usage", value=f"```{self.get_command_signature(command)}```", inline=False
        #)
        embed.set_footer(text='<arg>  means the argument is required\n[arg]  means the argument is optional')
        channel = self.get_destination()
        await channel.send(embed=embed)
	
    def add_subcommand_formatting(self, command):
    	fmt = '**{0}{1}** \N{EN DASH} {2}' if command.short_doc else '{0}{1}'
    	self.paginator.add_line(fmt.format(self.clean_prefix, command.qualified_name, command.short_doc))

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

    	await self.send_pages()

    def get_help(self, command, brief=True):
        """Gets the command short_doc if brief is True while getting the longer help if it is false"""
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
        embed = discord.Embed(title=self.get_command_signature(command), description=self.get_help(command, brief=False))
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=f'[{" | ".join(f"`{x}`" for x in alias)}]', inline=False)
        if isinstance(command, commands.Group):
            subcommand = command.commands
            value = "\n".join(self.get_command_signature(c) for c in subcommand, "\N{EN DASH}".join(command.short_doc)
            embed.add_field(name=plural("Subcommand(s)", len(subcommand)), value=value)

        return embed

    async def handle_help(self, command):
        with contextlib.suppress(commands.CommandError):
            await command.can_run(self.context)
            return await self.context.reply(embed=self.get_command_help(command), mention_author=False)
        raise CantRun("You don't have enough permission to see this help.") from None

    async def send_group_help(self, group):
        await self.handle_help(group)