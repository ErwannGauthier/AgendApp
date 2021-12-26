import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utility.functionUtil import have_admin_role

load_dotenv(dotenv_path="config")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!agenda ", intents=intents)


@bot.command()
@commands.guild_only()
@commands.check(have_admin_role)
async def load(ctx, extension):
    extension = extension.lower()
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"The cog `{extension}` has been loaded.")


@bot.command()
@commands.guild_only()
@commands.check(have_admin_role)
async def reload(ctx, extension):
    extension = extension.lower()
    try:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
    except:
        bot.load_extension(f"cogs.{extension}")

    await ctx.send(f"The cog `{extension}` has been reloaded.")


@bot.command()
@commands.guild_only()
@commands.check(have_admin_role)
async def unload(ctx, extension):
    extension = extension.lower()
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"The cog `{extension}` has been unloaded.")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv("TOKEN"))
