from discord.ext import commands
import discord

async def send(ctx, text):
	embed=discord.Embed(description=text[:2048], color=0x9c5cb4, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)
	