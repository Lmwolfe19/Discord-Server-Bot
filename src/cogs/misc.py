import discord
from discord.ext import commands

class Miscellaneous(commands.Cog):
    def __init__ (self, client):
         self.client = client


    @commands.command(pass_context=True)
    async def hb(self, ctx):
        """Prints a Happy Birthday message. Use: '.hb <name>'"""
        message = ctx.message.content[3:]
        await ctx.message.delete()
        await ctx.send(f'Happy Birthday{message}')


def setup(client):
    client.add_cog(Miscellaneous(client))