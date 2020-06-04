import os
import discord
from discord.ext import tasks, commands
from os import listdir

#client
bot = commands.Bot(command_prefix="/", description="muug's personal bot for success")

#cog commands
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Everyone please welcome the filthy weeaboo {0.mention}. If you want a list of commands type /commands'.format(member))

    @commands.command()
    async def commands(self, ctx, *, member: discord.Member = None):
        """Gives out command list"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello there {0.name} ~ I am a music bot that queries youtube 4 u ... current commands are: \n         /play <youtube search>\nor try /playmusic <youtube search> to stream audio to your channel '
            .format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

def setup(bot):
    bot.add_cog(Utility(bot))
