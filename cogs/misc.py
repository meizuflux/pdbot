from discord.ext import commands
import discord
import random
import inspect
import os
import json
from pkg_resources import get_distribution
import time
import typing
import humanize
import platform
import pathlib
import psutil
import utils.embed as qembed


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

    @commands.command()  
    async def snipe(self, ctx, *, channel: typing.Union[discord.TextChannel, discord.Member] = None):
        try:
            if isinstance(channel, discord.TextChannel):
                msg = self.bot.snipes[channel.id]

            if isinstance(channel, discord.Member):
                msg = self.bot.snipes[channel.id]

            if not channel:
                l = ctx.channel or channel
                msg = self.bot.snipes[l.id]

        except KeyError:
            return await qembed.send(ctx, 'Nothing to snipe!')

        await ctx.send(embed=discord.Embed(description=msg.content, color=self.bot.embed_color, timestamp=msg.created_at).set_author(name=str(msg.author), icon_url=str(msg.author.avatar_url)).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url))

    @commands.command()  
    async def snipeedit(self, ctx, *, channel: typing.Union[discord.TextChannel, discord.Member] = None):
        try:
            if isinstance(channel, discord.TextChannel):
                msg = self.bot.edits[channel.id]

            if isinstance(channel, discord.Member):
                msg = self.bot.edits[channel.id]

            if not channel:
                msg = self.bot.edits[ctx.channel.id]
            m = await ctx.fetch_message(msg.id)
            
        except KeyError:
            return await qembed.send(ctx, 'Nothing to snipe!')

        await ctx.send(embed=discord.Embed(color=self.bot.embed_color, timestamp=msg.created_at).add_field(name='Before:', value=msg.content, inline=False).add_field(name='After:', value=m.content).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url).set_author(name=str(msg.author), icon_url=str(msg.author.avatar_url)))

    @snipeedit.error
    async def snipeedit_error(self, ctx, error):
        if isinstance(error, discord.HTTPException):
            await qembed.send(ctx, 'Nothing to snipe!')
        if isinstance(error, commands.CommandInvokeError):
            await qembed.send(ctx, 'Nothing to snipe!')
        else:
            raise error

    @commands.command(aliases=['avatar'],
                      help='Gets the profile picture of a user')
    async def pfp(self, ctx, *, user: discord.Member = None):
        if not user:
            user = ctx.author
        e = discord.Embed(title=f'Profile Picture for {user.name}', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        e.set_image(url=user.avatar_url)
        await ctx.send(embed=e)

    @commands.command(name='puppy',
                      help='A cute little puppy doing cute things')
    async def puppy(self, ctx):
        await qembed.send(
            ctx,
            'https://www.youtube.com/watch?v=j5a0jTc9S10&list=PL3KnTfyhrIlcudeMemKd6rZFGDWyK23vx&index=11'
        )



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
                          color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e, delete_after=2)

    @commands.command(help='Purges a set amount of messages by the bot', brief='Purges bot messages')
    @mng_msg()
    async def botpurge(self, ctx, amount: int):
        if amount > 75:
            return await qembed.send(ctx, 'Please keep the amount of messages to purge under 75.')
        def is_me(m):
            return m.author == self.bot.user
        deleted = await ctx.channel.purge(limit=amount, check=is_me)
        await ctx.send('Deleted {} message(s)'.format(len(deleted)))

    # from pb https://github.com/PB4162/PB-Bot
    @commands.command(aliases=["rawmessage", "rawmsg"])
    async def raw_message(self, ctx, *, message: discord.Message = None):
        """
        Get the raw info for a message.
        `message` - The message.
        """
        message = message or ctx.message

        try:
            msg = await self.bot.http.get_message(ctx.channel.id, message.id)
        except discord.NotFound:
            return await ctx.send("Sorry, I couldn't find that message.")

        raw = json.dumps(msg, indent=4)
        if len(raw) > 1989:
            return await qembed.send(ctx, 'Sorry, the message was too long')
        await qembed.send(ctx, f"```json\n{raw}```")

    @commands.command(help='Builds an embed from a dict. You can use https://eb.nadeko.bot/ to get one', brief='Builds an embed', aliases=['make_embed', 'embed_builder'])
    async def embedbuilder(self, ctx, *, embed: json.loads):
        try:
            await ctx.send(embed=discord.Embed().from_dict(embed))
        except:
            await qembed.send(ctx, 'You clearly don\'t know what this is')

    @commands.command(help='A link to invite the bot to your server')
    async def invite(self, ctx):
        await qembed.send(
            ctx,
            f'https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=205388999'
        )

    @commands.command(help='Sends the docs for my API')
    async def potatoapi(self, ctx):
        e = discord.Embed(title='PotatoAPI',
                          description='https://www.potatoapi.ml/docs',
						  color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
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
            color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        if len(mention_roles) == 0:
            embed.add_field(name='Roles', value='This user has no roles')
        else:
            embed.add_field(name='Top Role', value=member.top_role.mention)
            embed.add_field(name='Roles',
                            value=', '.join(mention_roles),
                            inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo',
                      usage='',
                      help='Shows info about the server.')
    @commands.guild_only()
    async def sinfo(self, ctx):
        guild = ctx.guild
        roles = [role.name.replace('@', '@\u200b') for role in guild.roles]
        e = discord.Embed(color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
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
                description='https://pypi.org/project/discord-pretty-help/', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        elif command.startswith('jsk') or command.startswith('jishaku'):
            e = discord.Embed(description='https://pypi.org/project/jishaku/', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
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
							  color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            e.set_footer(text='Don\'t forget the Licence!')
            await ctx.send(embed=e)




def setup(bot):
    bot.add_cog(Misc(bot))
