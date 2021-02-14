import discord
from discord.ext import commands
import os
import asyncdagpi
import aiohttp
import re
import datetime
from keep_alive import keep_alive
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MongoDB'])
db = client.prefixes


async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("c//")(bot, message)

    try:
        data = await db.pre.find_one({"_id": message.guild.id})
        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            await db.pre.insert_one({"_id": message.guild.id, "prefix": "c//"})
            return commands.when_mentioned_or("c//")(bot, message)
        return commands.when_mentioned_or(data['prefix'])(bot, message)
    except:
        return commands.when_mentioned_or("c//")(bot, message)


class Cute(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            intents=intents,
            owner_ids={809587169520910346},
            description=
            '```py\n  ____      _       \n / ___|   _| |_ ___ \n| |  | | | | __/ _ \n| |__| |_| | ||  __/\n \____\__,_|\__\___|```'
        )
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()
        self.author_id = 809587169520910346
        self.dagpi = asyncdagpi.Client(os.environ['dagpikey'])
        self.session = aiohttp.ClientSession()
        self.embed_color = 0x9c5cb4  #0x1E90FF
        self.mongo = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MongoDB'])
        self.data = self.mongo.data

    def starter(self):
        self.start_time = datetime.datetime.utcnow()
        extensions = [
            'cogs.misc', 'cogs.fun', 'cogs.tenor', 'cogs.devcommands',
            'cogs.tracking', 'cogs.speak', 'cogs.api', 'cogs.errorhandler',
            'cogs.owner', 'cogs.prefixes', 'jishaku', 'cogs.beatsaber',
            'cogs.imagemanip', 'cogs.invites', 'cogs.mongo', 'cogs.zane',
            'cogs.eco', 'cogs.useful'
        ]
        for extension in extensions:
            self.load_extension(extension)

        keep_alive()
        self.run(os.environ['DTOKEN'])

    async def get_context(self, message: discord.Message, *, cls=None):
            return await super().get_context(message, cls=cls or commands.Context)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if re.fullmatch(f"^(<@!?{self.user.id}>)\s*", message.content):
            await message.add_reaction('<:what:791007602745671701>')
            ctx = await self.get_context(message)
            return await ctx.invoke(self.get_command("botprefix"))
        await self.process_commands(message)


bot = Cute()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!\nGuilds: {len(bot.guilds)}\nMembers: {str(sum([guild.member_count for guild in bot.guilds]))}')

if __name__ == "__main__":
    bot.starter()
