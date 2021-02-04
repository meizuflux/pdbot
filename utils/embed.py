from discord.ext import commands
import discord

async def send_in_embed(ctx, text):
	embed=discord.Embed(description=text[:2048], color=0x9c5cb4)
	await ctx.send(embed=embed)