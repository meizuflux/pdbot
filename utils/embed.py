import discord

async def send(ctx, text):
    bot = ctx.bot
    embed=discord.Embed(description=text[:2048], color=bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
	