import asyncio
import os
import time

import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} extension loaded.')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} extension unloaded.')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} extension reloaded.')


for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print('Bot is ready.')

#@client.event
#async def on_message(ctx):
#    if(str(ctx.author) == "Hal9000#0673"):
 #       time.sleep(5)
 #       await ctx.delete()
 #       time.sleep(30)

@client.command()
@commands.has_guild_permissions()
async def clear(ctx, amount = 5):
    if len(ctx.message.content) > 6:
        try:
            amount = int(ctx.message.content[6:])
        except ValueError:
            await ctx.send('Proper format: .clear <integer>')

    await ctx.channel.purge(limit = amount + 1)
    await ctx.send(f"{amount} message(s) cleared.")

    await asyncio.sleep(5)
    await ctx.channel.purge(limit = 1)

@client.command()
async def poll(ctx):
    channel = ctx.channel

    # Store message here and delete it from channel.
    message = ctx.message
    await ctx.message.delete()

    # Ping everyone and post poll.
    await channel.send('@everyone')
    msg = await channel.send(message.content[6:])

    # Add reactions to poll.
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

# Private AUTH code. Do not share with anyone or change.
client.run('Removed for git upload...')
