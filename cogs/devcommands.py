import discord
from discord.ext import commands
import os
from utils import default


class DevCommands(commands.Cog, name='Developer Commands', command_attrs=dict(hidden=True)):
	'''These are the developer commands'''

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):  
		'''
		The default check for this cog whenever a command is used. Returns True if the command is allowed.
		'''
		return ctx.author.id == self.bot.author_id

	@commands.command(  # Decorator to declare where a command is.
		name='reload',  # Name of the command, defaults to function name.
		aliases=['rl']  # Aliases for the command.
	)  
	async def reload(self, ctx, cog):
		'''
		Reloads a cog.
		'''
		extensions = self.bot.extensions  # A list of the bot's cogs/extensions.
		if cog in extensions:
			self.bot.unload_extension(cog)  # Unloads the cog
			self.bot.load_extension(cog)  # Loads the cog
			await ctx.send('Done')  # Sends a message where content='Done'
		else:
			await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.

	@commands.command()
	async def reloadall(self, ctx):
	    """ Reloads all extensions. """
	    error_collection = []
	    for file in os.listdir("cogs"):
	        if file.endswith(".py"):
	            name = file[:-3]
	            try:
	                self.bot.reload_extension(f"cogs.{name}")
	            except Exception as e:
	                error_collection.append(
	                    [file, default.traceback_maker(e, advance=False)]
                    )

	    if error_collection:
	        output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
	        return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

	    await ctx.send("Successfully reloaded all extensions")
	
	@commands.command(name="unload", aliases=['ul']) 
	async def unload(self, ctx, cog):
		'''
		Unload a cog.
		'''
		extensions = self.bot.extensions
		if cog not in extensions:
			await ctx.send("Cog is not loaded!")
			return
		self.bot.unload_extension(cog)
		await ctx.send(f"`{cog}` has successfully been unloaded.")
	
	@commands.command(name="load")
	async def load(self, ctx, cog):
		'''
		Loads a cog.
		'''
		try:

			self.bot.load_extension(cog)
			await ctx.send(f"`{cog}` has successfully been loaded.")

		except commands.errors.ExtensionNotFound:
			await ctx.send(f"`{cog}` does not exist!")

	@commands.command(name="listcogs", aliases=['lc'])
	async def listcogs(self, ctx):
		'''
		Returns a list of all enabled commands.
		'''
		base_string = "```css\n"  # Gives some styling to the list (on pc side)
		base_string += "\n".join([str(cog) for cog in self.bot.extensions])
		base_string += "\n```"
		await ctx.send(base_string)



def setup(bot):
	bot.add_cog(DevCommands(bot))