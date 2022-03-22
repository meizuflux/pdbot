import discord
import traceback
import sys
from utils import default
from discord.ext import commands
import json
import humanize
import utils.embed as qembed


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        if cog := ctx.cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, ) #if you want to not send error messages
        #ignored = ()

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandNotFound):
            #await qembed.send(ctx, f'`{ctx.command}` was not found.')
            pass

        elif isinstance(error, commands.CheckFailure):
            return await qembed.send(
                ctx,
                f'You do not have the correct permissions for `{ctx.command}`')

        if isinstance(error, discord.Forbidden):
            return await qembed.send(
                ctx,
                f'I do not have the correct permissions for `{ctx.command}`')

        elif isinstance(error, commands.CommandOnCooldown):
            return await qembed.send(
                ctx,
                f"This command is on cooldown.\nTry again in {humanize.precisedelta(error.retry_after, minimum_unit='seconds')}"
            )

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                e = discord.Embed(
                    description=
                    f'`{ctx.command}` can not be used in Private Messages.',
                    color=self.bot.embed_color)
                return await ctx.author.send(embed=e)
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingRequiredArgument):
            return await qembed.send(ctx, f'{error}')

        elif isinstance(error, commands.DisabledCommand):
            return await qembed.send(ctx, f'`{ctx.command}` has been disabled.')

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                return await qembed.send(ctx, 
                    'I could not find that member. Please try again.')

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error),
                                      error,
                                      error.__traceback__,
                                      file=sys.stderr)
            error_collection = [[default.traceback_maker(error, advance=False)]]
            output = "\n".join(
                [f"```diff\n- {g[0]}```" for g in error_collection])
            await qembed.send(ctx, f"{output}\n¯\_(ツ)_/¯")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
