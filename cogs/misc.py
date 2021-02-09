from discord.ext import commands
import discord
import random
import inspect
import os
from pkg_resources import get_distribution
import time
import humanize
import platform
import pathlib
import psutil
import utils.embed as qembed
import motor.motor_asyncio


class Misc(commands.Cog):
    """For commands that don't really have a category"""
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    def mng_msg():
        def predicate(ctx):
            if ctx.author.id == 777893499471265802:
                return True
            if ctx.guild:
                if ctx.author.guild_permissions.manage_messages == True:
                    return True
            else:
                return False

        return commands.check(predicate)

    @commands.command(aliases=['avatar'],
                      help='Gets the profile picture of a user')
    async def pfp(self, ctx, *, user: discord.Member = None):
        if not user:
            user = ctx.author
        e = discord.Embed(title=f'Profile Picture for {user.name}', color=self.bot.embed_color)
        e.set_image(url=user.avatar_url)
        await ctx.send(embed=e)

    @commands.command(name='puppy',
                      help='A cute little puppy doing cute things')
    async def puppy(self, ctx):
        await qembed.send(
            ctx,
            'https://www.youtube.com/watch?v=j5a0jTc9S10&list=PL3KnTfyhrIlcudeMemKd6rZFGDWyK23vx&index=11'
        )

    @commands.command(name='ping', help='only for cool kids')
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send("Pinging ...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        dbstart = time.perf_counter()
        await self.bot.prefix_db.pre.find_one({"_id": str(ctx.guild.id)})
        dbend = time.perf_counter()
        dbduration = (dbend - dbstart) * 1000
        pong = discord.Embed(title='Ping', color=self.bot.embed_color)
        pong.add_field(name='Typing Latency',
                       value=f'```python\n{round(duration)} ms```')
        pong.add_field(
            name='Websocket Latency',
            value=f'```python\n{round(self.bot.latency * 1000)} ms```')
        pong.add_field(name='Database Latency',
                       value=f'```python\n{round(dbduration)} ms```')
        await message.edit(content=None, embed=pong)

    @commands.command(name='creator', help='Checks if you are the creator')
    async def creator(self, ctx):
        thelist = [
            '<:sad:790608581615288320>', '<:DogKek:790932497856725013>',
            '<:4Head:790667956963115068>', '<:Sadge:789590510225457152>'
        ]
        if ctx.author.id == self.bot.author_id:
            await qembed.send(ctx, 'you <:PogYou:791007602741739610>')
        else:
            await qembed.send(ctx, f'not you {random.choice(thelist)}')

    @commands.command(
        name='purge',
        help=
        'Purges a set amount of messages in a channel. You and the bot must have manage messages permissions.',
        brief='Purges a set amount of messages.')
    @commands.guild_only()
    @mng_msg()
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=1 + int(amount))
        e = discord.Embed(description=f'Deleted {amount} message(s)',
                          color=self.bot.embed_color)
        await ctx.send(embed=e, delete_after=2)

    @commands.command(help='A link to invite the bot to your server')
    async def invite(self, ctx):
        await qembed.send(
            ctx,
            'https://discord.com/oauth2/authorize?client_id=777964578776285194&scope=bot&permissions=8'
        )

    @commands.command(help='Sends the docs for my API')
    async def potatoapi(self, ctx):
        e = discord.Embed(title='PotatoAPI',
                          description='https://www.potatoapi.ml/docs',
						  color=self.bot.embed_color)
        await ctx.send(embed=e)

    @commands.command(name='activity',
                      aliases=['a', 'presence'],
                      help='Changes the bot presence. Owner only.',
                      hidden=True)
    @commands.is_owner()
    async def presence(self, ctx, atype: str, *, activity=None):
        atype = atype.lower()
        if atype == 'default':
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening,
                                          name=f'@{self.bot.user.name}'))
        if atype == 'watching':
            await self.bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching, name=activity))
        if atype == 'listening':
            await self.bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.listening, name=activity))
        if atype == 'playing':
            await self.bot.change_presence(activity=discord.Game(name=activity)
                                           )
        if atype == 'streaming':
            await self.bot.change_presence(activity=discord.Streaming(
                name=activity, url='https://twitch.tv/ppotatoo_'))
        if atype == 'competing':
            await self.bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.competing, name=activity))
        await qembed.send(
            ctx, f'Set activity to `{activity}` with type `{atype}` ')

    @commands.command(name='whois',
                      aliases=['ui', 'userinformation'],
                      help='Gets info about a user.')
    async def who(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        mention_roles = [i.mention for i in member.roles[1:]]
        join = member.joined_at.strftime("%m/%d/%Y")
        create = member.created_at.strftime("%m/%d/%Y")
        embed = discord.Embed(
            title=str(member),
            description=f'**Joined:** {join}\n**Account Creation:** {create}',
            color=self.bot.embed_color)
        embed.set_thumbnail(url=member.avatar_url)
        if len(mention_roles) == 0:
            embed.add_field(name='Roles', value='This user has no roles')
        else:
            embed.add_field(name='Top Role', value=member.top_role.mention)
            embed.add_field(name='Roles',
                            value=', '.join(mention_roles),
                            inline=False)
        if member.name != member.display_name:
            embed.set_footer(text=f'{member.id} • {member.display_name}')
        else:
            embed.set_footer(text=member.id)
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo',
                      usage='',
                      help='Shows info about the server.')
    @commands.guild_only()
    async def sinfo(self, ctx):
        guild = ctx.guild
        roles = [role.name.replace('@', '@\u200b') for role in guild.roles]
        e = discord.Embed(color=self.bot.embed_color)
        e.title = guild.name
        e.description = f'**ID:** {guild.id}'
        e.set_thumbnail(url=ctx.guild.icon_url)
        fmt = f'Total: {guild.member_count}'
        e.add_field(name='Members', value=fmt, inline=False)
        e.add_field(name='Roles',
                    value=', '.join(roles)
                    if len(roles) < 10 else f'{len(roles)} roles')
        e.set_footer(text='Created').timestamp = guild.created_at
        await ctx.send(embed=e)

    @commands.command(help='Gets the link to the source of a command',
                      brief='Gets the source of a command')
    async def source(self, ctx, *, command: str = None):
        source_url = 'https://github.com/ppotatoo/pdbot'
        branch = 'master'
        if command is None:
            return await ctx.send(source_url)
        if command == 'help':
            e = discord.Embed(
                description='https://pypi.org/project/discord-pretty-help/', color=self.bot.embed_color)
            await ctx.send(embed=e)
        elif command.startswith('jsk') or command.startswith('jishaku'):
            e = discord.Embed(description='https://pypi.org/project/jishaku/', color=self.bot.embed_color)
            await ctx.send(embed=e)
        else:
            obj = self.bot.get_command(command.replace('.', ' '))
            if obj is None:
                return await ctx.send('Could not find command.')
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

            lines, firstlineno = inspect.getsourcelines(src)
            if not module.startswith('discord'):
                location = os.path.relpath(filename).replace('\\', '/')
            else:
                location = module.replace('.', '/')
                source_url = 'https://github.com/ppotatoo/pdbot'
                branch = 'master'

            final_url = f'<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>'
            e = discord.Embed(title='Add a star if you like!',
                              description=final_url,
							  color=self.bot.embed_color)
            e.set_footer(text='Don\'t forget the Licence!')
            await ctx.send(embed=e)

    @commands.command(aliases=['information', 'botinfo'],
                      help='Gets info about the bot')
    async def info(self, ctx):
        msg = await ctx.send('Getting bot information ...')
        avgmembers = sum([guild.member_count
                          for guild in self.bot.guilds]) / len(self.bot.guilds)
        #ramPerc = psutil.virtual_memory().percent
        cpuUsage = psutil.cpu_percent()
        cpuFreq = psutil.cpu_freq().current
        #memory_usage = self.process.memory_full_info().uss / 1024**2
        #cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
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

        emb = discord.Embed(colour=self.bot.embed_color)
        #emb.set_thumbnail(url=self.bot.user.avatar_url)
        emb.set_author(name=self.bot.user.name,
                       url='https://github.com/ppotatoo/pdbot',
                       icon_url=self.bot.user.avatar_url)
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        emb.add_field(name='Developer',
                      value=f'```ppotatoo#6862 (777893499471265802)```',
                      inline=False)
        emb.add_field(
            name='<:online:801444524148523088> Uptime',
            value=
            f'[Check Bot Status](https://stats.uptimerobot.com/Gzv84sJ9oV \"UptimeRobot\")\n```{humanize.precisedelta(self.bot.start_time, format="%0.0f")}```',
            inline=False)
        emb.add_field(name='Hosting', value=f'```{hosting}```', inline=False)

        emb.add_field(name='CPU Usage',
                      value=f'```{cpuUsage:.2f}%```',
                      inline=True)
        emb.add_field(name='CPU Frequency',
                      value=f'```{cpuFreq} MHZ```',
                      inline=True)
        emb.add_field(name='Memory Usage',
                      value=f'```{ramusage}```',
                      inline=True)

        emb.add_field(name='<:python:801444523623710742> Python Version',
                      value=f'```{pyVersion}```',
                      inline=True)
        emb.add_field(
            name='<:discordpy:801444523854135307> Discord.py Version',
            value=f'```{libVersion}```',
            inline=True)

        emb.add_field(name='Line Count',
                      value=f'```{ls:,} lines```',
                      inline=False)
        emb.add_field(
            name='Command Count',
            value=f'```{len(set(self.bot.walk_commands()))-31} commands```',
            inline=True)
        emb.add_field(
            name='Command Use:',
            value=f'```{self.bot.counter-1} commands since reboot```',
            inline=True)
        emb.add_field(name='Guild Count',
                      value=f'```{str(len(self.bot.guilds))} guilds```',
                      inline=False)

        emb.add_field(
            name='Member Count',
            value=
            f'```{str(sum([guild.member_count for guild in self.bot.guilds]))} members```',
            inline=True)
        emb.add_field(name='Average Member Count',
                      value=f'```{avgmembers:.0f} members per guild```')

        emb.set_footer(text=f'{ctx.author} • {ctx.author.id}',
                       icon_url=ctx.author.avatar_url)

        await msg.edit(content=None, embed=emb)


def setup(bot):
    bot.add_cog(Misc(bot))
