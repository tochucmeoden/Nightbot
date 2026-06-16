import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="N!", intents=intents)

@bot.event
async def on_ready():
    print(f"NightBot đã đăng nhập: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command(name="cf")
async def coinflip(ctx):
    result = random.choice(["🪙 Mặt ngửa!", "🌑 Mặt sấp!"])
    await ctx.send(f"**Kết quả tung đồng xu:**\n{result}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Đã xóa {amount} tin nhắn.")
    await msg.delete(delay=3)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"👑 Đã cấp role {role.name} cho {member.mention}")

@bot.command()
async def bj(ctx):
    player = random.randint(15, 21)
    dealer = random.randint(15, 21)

    if player > 21:
        result = "💥 Bạn quắc!"
    elif dealer > 21 or player > dealer:
        result = "🎉 Bạn thắng!"
    elif player == dealer:
        result = "🤝 Hòa!"
    else:
        result = "😿 Bạn thua!"

    await ctx.send(
        f"🃏 **Xì dách**\n"
        f"Bạn: {player}\n"
        f"NightBot: {dealer}\n\n"
        f"{result}"
    )

bot.run("MTUxNjM2MTM0Mjk5NzQ5OTk1Ng.GYCUGI.2feiO6zbOL558NwPMckLkG6WYOaQGF2I_X3F6k")
