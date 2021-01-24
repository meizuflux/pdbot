import discord
import traceback
import sys
from utils import default
from discord.ext import commands
import json


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.

        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(error)

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)

        if isinstance(error, commands.CheckFailure):
            await ctx.send(
                'You do not have the correct permissions for this command')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send(
                    'I could not find that member. Please try again.')

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print(
                'Ignoring exception in command {}:'.format(ctx.command),
                file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            with open("prefixes.json", "r") as f:
                prefix = json.load(f)
            error_collection = []
            error_collection.append(
	                    [default.traceback_maker(error, advance=False)]
                    )
            output = "\n".join([f"```diff\n- {g[0]}```" for g in error_collection])
            await ctx.send(
                f"{output}\n Try doing ```python\n{prefix[str(ctx.guild.id)]}help {ctx.command}\n```"
            )


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
