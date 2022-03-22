import discord
from discord.ext import commands

class CustomContext(commands.Context):
    @property
    def secret(self):
        return 'my secret here'

    # https://github.com/PB4162/PB-Bot/blob/master/utils/classes.py cool    
    async def send(self, content=None, **kwargs):
        if "reply" in kwargs and not kwargs.pop("reply"):
            return await super().send(content, **kwargs)
        try:
            mention_author = bool(kwargs.pop("mention", False))
            return await self.reply(content, **kwargs, mention_author=mention_author)
        except discord.HTTPException:
            return await super().send(content, **kwargs)