import discord
from discord.ext import commands
import yt_dlp
import asyncio
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=['!', '!'], intents=intents)

# قائمة التشغيل
queue = {}
current_playing = {}
is_paused = {}

# إعدادات yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'no_warnings': True,
}

@bot.event
async def on_ready():
    print(f'✅ {bot.user} متصل وجاهز!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!play"))

# أوامر التشغيل
@bot.command(name='play', aliases=['p', 'P', 'Play'])
async def play(ctx, *, query):
    """تشغيل أغنية"""
    try:
        if not ctx.author.voice:
            await ctx.send("❌ يجب أن تكون في قناة صوتية!")
            return
            
        channel = ctx.author.voice.channel
        
        if ctx.voice_client is None:
            vc = await channel.connect()
        else:
            vc = ctx.voice_client
        
        await ctx.send(f"🎵 جاري البحث عن: `{query}`...")
        
        # محاكاة التشغيل
        await ctx.send(f"▶️ الآن يتم تشغيل: `{query}`")
        
    except Exception as e:
        await ctx.send(f"❌ خطأ: {str(e)}")

# أوامر الإيقاف
@bot.command(name='stop', aliases=['s', 'S', 'Stop'])
async def stop(ctx):
    """إيقاف التشغيل"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ تم إيقاف البوت")
    else:
        await ctx.send("❌ البوت غير متصل بقناة صوتية!")

@bot.command(name='skip', aliases=['Skip'])
async def skip(ctx):
    """تخطي الأغنية الحالية"""
    await ctx.send("⏭️ تم تخطي الأغنية")

# أوامر مستوى الصوت
@bot.command(name='volume', aliases=['v', 'V'])
async def volume(ctx, level: int):
    """تعديل مستوى الصوت (1-100)"""
    if 1 <= level <= 100:
        await ctx.send(f"🔊 تم تعديل مستوى الصوت إلى: {level}%")
    else:
        await ctx.send("❌ المستوى يجب أن يكون بين 1 و 100")

@bot.command(name='help')
async def help_command(ctx):
    """قائمة الأوامر"""
    embed = discord.Embed(
        title="🎵 أوامر البوت الموسيقى",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="▶️ أوامر التشغيل",
        value="`!play` أو `!p` أو `!P` - تشغيل أغنية",
        inline=False
    )
    
    embed.add_field(
        name="⏹️ أوامر الإيقاف",
        value="`!stop` أو `!s` أو `!S` - إيقاف التشغيل\n`!skip` - تخطي الأغنية",
        inline=False
    )
    
    embed.add_field(
        name="🔊 أوامر الصوت",
        value="`!volume` أو `!v` - تعديل مستوى الصوت (1-100)",
        inline=False
    )
    
    await ctx.send(embed=embed)

# تشغيل البوت
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ لم يتم العثور على DISCORD_TOKEN")
