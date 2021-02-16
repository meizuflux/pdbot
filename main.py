import discord
from discord.ext import commands
import os
import asyncdagpi
import aiohttp
import re
import asyncpg
import datetime
from keep_alive import keep_alive
import motor.motor_asyncio
from utils.context import CustomContext

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MongoDB'])
db = client.prefixes
dsn = os.environ['sqldsn']


class Cute(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        super().__init__(
            command_prefix=self.get_prefix,
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
        self.default_prefix = 'c//'
        self.prefixes = {}

    async def get_prefix(bot, message):
        if message.guild == None:
            return commands.when_mentioned_or(bot.default_prefix)(bot, message)
        try:
            return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)
        except KeyError:
            prefix = await bot.db.fetchval("SELECT prefix FROM prefixes WHERE serverid = $1", message.guild.id)
            if prefix:
                bot.prefixes[message.guild.id] = prefix
                return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)
            else:
                await bot.db.execute("INSERT INTO prefixes(serverid,prefix) VALUES($1,$2) ON CONFLICT (serverid) DO UPDATE SET prefix = $2",message.guild.id, bot.default_prefix)
                bot.prefixes[message.guild.id] = bot.default_prefix
                return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)

    async def try_user(self, user_id: int) -> discord.User:
        user = self.get_user(user_id)
        if not user:
            user = await self.fetch_user(user_id)
        return user.name

    async def create_tables(self):
        await self.wait_until_ready()
        await self.db.execute("CREATE TABLE IF NOT EXISTS prefixes (serverid BIGINT PRIMARY KEY,prefix VARCHAR(50))")
        await self.db.execute("CREATE TABLE IF NOT EXISTS scoresaber (userid BIGINT PRIMARY KEY,ssid BIGINT)")
        await self.db.execute("CREATE TABLE IF NOT EXISTS economy (userid BIGINT PRIMARY KEY,wallet BIGINT,bank BIGINT)")

    def starter(self):
        try:
            print("Connecting to database ...")
            pool_pg = self.loop.run_until_complete(asyncpg.create_pool(dsn=dsn))
            print("Connected to PostgreSQL server!")
        except Exception as e:
            print("Could not connect to database:", e)
        else:
            print("Connecting to Discord ...")
            self.start_time = datetime.datetime.utcnow()
            self.db = pool_pg
            extensions = [
            'cogs.misc', 'cogs.fun', 'cogs.tenor', 'cogs.devcommands',
            'cogs.tracking', 'cogs.speak', 'cogs.api', 'cogs.errorhandler',
            'cogs.owner', 'cogs.prefixes', 'jishaku', 'cogs.beatsaber',
            'cogs.imagemanip', 'cogs.invites', 'cogs.zane',
            'cogs.eco', 'cogs.useful'
            ]
            for extension in extensions:
                self.load_extension(extension)
            
            keep_alive()
            self.run(os.environ['DTOKEN'])

    async def get_context(self, message: discord.Message, *, cls=None):
            return await super().get_context(message, cls=cls or CustomContext)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if re.fullmatch(f"^(<@!?{self.user.id}>)\s*", message.content):
            await message.add_reaction('<:what:791007602745671701>')
            try:
                sprefix = bot.prefixes[message.guild.id]
            except KeyError:
                prefix = await bot.db.fetchval("SELECT prefix FROM prefixes WHERE serverid = $1", message.guild.id)
                if prefix:
                    sprefix = prefix
                else:
                    sprefix = bot.default_prefix
            await message.channel.send("My prefix on `{}` is `{}`".format(message.guild.name, sprefix))
        await self.process_commands(message)





bot = Cute()
bot.loop.create_task(bot.create_tables())
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!\nGuilds: {len(bot.guilds)}\nMembers: {str(sum([guild.member_count for guild in bot.guilds]))}')

if __name__ == "__main__":
    bot.starter()
