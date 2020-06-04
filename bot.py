import os
import sys
import discord
import config
import youtube_dl
import ffmpeg
from discord.ext import commands, tasks
from youtube_api import YouTubeDataAPI

#globals pulled from config and such
token = config.config["token"]
prefix = config.config["prefix"]
key = config.config["key"]
yt = YouTubeDataAPI(key)

#creates cog subdirectory path for easy expansion into a sub directory... feel free to add your own
sys.path.insert(0, './cogs')

#client from discord api and cog extensions load up on le stack
bot = commands.Bot(command_prefix="/", description="lpg personal bot for success")
bot.load_extension('utility')
bot.load_extension('media')

#on startup this clears server audio files... you're going to want to keep this ^^
for root, dirs, files in os.walk('.'):
    for fname in files:
        if fname.endswith('.webm'):
            os.remove(os.path.join(root, fname))

#startup command from above but looped on task... this can stop a stream so don't shorten too much. when you host a bot 24/7 this stops the bots serverfrom being overloaded with dl's
@tasks.loop(minutes=300, count=1)
async def clear_files():
    for root, dirs, files in os.walk('.'):
        for fname in files:
            if fname.endswith('.webm'):
                os.remove(os.path.join(root, fname))

#same as above boio
@clear_files.after_loop
async def after_clear_files():
    print('youtube_dl files are cleared from the server every 300 minutes. Head to utility file in ./cogs to add more tasks!')

#core audio/video command if cogs fail during development you can still query youtube search engine and post the top search. if you're going to expand into playlists, you'll want to mess with this function
@bot.command(pass_context=True)
async def play(ctx, *, query):
    searches = yt.search(query, max_results=1)
    res = list(searches[0].values())[0] 
    url = "https://www.youtube.com/watch?v=" + str(res)
    await ctx.send(url)

#ready up && events
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    
bot.run(token)
