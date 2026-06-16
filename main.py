import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os
import time
import asyncio

# ======================
# INTENTS
# ======================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="N!", intents=intents)

OWNER_ID = 1301466547209895960

# ======================
# DATA SYSTEM
# ======================
FILE = "data.json"

def load():
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

data = load()

def save():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user(uid):
    uid = str(uid)
    if uid not in data:
        data[uid] = {"coin": 1000}
    return uid

# ======================
# READY + SYNC SLASH
# ======================
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"✅ BOT ONLINE: {bot.user}")
    except Exception as e:
        print("SLASH ERROR:", e)

# ======================
# PREFIX HANDLER
# ======================
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# ======================
# 💰 COIN
# ======================
@bot.command()
async def coin(ctx):
    uid = get_user(ctx.author.id)
    await ctx.send(f"💰 {data[uid]['coin']} coin")

# ======================
# 🎁 DAILY
# ======================
daily_cd = {}

@bot.command()
async def daily(ctx):
    uid = str(ctx.author.id)
    now = time.time()

    get_user(ctx.author.id)

    if uid in daily_cd and now - daily_cd[uid] < 86400:
        return await ctx.send("⏳ Bạn đã nhận rồi")

    reward = random.randint(200, 600)
    data[uid]["coin"] += reward
    daily_cd[uid] = now
    save()

    await ctx.send(f"🎁 +{reward} coin")

# ======================
# 🎰 COIN FLIP (TUNG XU)
# ======================
@bot.command()
async def cf(ctx, bet: int, choice: str):
    uid = get_user(ctx.author.id)

    if choice not in ["head", "tail"]:
        return await ctx.send("❌ N!cf 100 head/tail")

    if data[uid]["coin"] < bet:
        return await ctx.send("❌ Không đủ coin")

    msg = await ctx.send("🪙 Đang tung xu...")

    await asyncio.sleep(2)

    result = random.choice(["head", "tail"])

    if result == choice:
        data[uid]["coin"] += bet * 2
        text = f"🎉 WIN ({result}) +{bet*2}"
    else:
        data[uid]["coin"] -= bet
        text = f"💥 LOSE ({result}) -{bet}"

    save()

    await msg.edit(content=f"🪙 KẾT QUẢ: {text}")

# ======================
# 🃏 BLACKJACK
# ======================
@bot.command()
async def bj(ctx, bet: int):
    uid = str(ctx.author.id)

    if data[uid]["coin"] < bet:
        return await ctx.send("❌ Không đủ coin")

    player = random.randint(10, 21)
    bot_hand = random.randint(10, 21)

    while bot_hand < 17:
        bot_hand += random.randint(1, 10)

    if player > 21:
        result = "💥 Thua"
        data[uid]["coin"] -= bet

    elif bot_hand > 21 or player > bot_hand:
        result = "🎉 Thắng"
        data[uid]["coin"] += bet

    elif player == bot_hand:
        result = "🤝 Hòa"

    else:
        result = "💥 Thua"
        data[uid]["coin"] -= bet

    save()

    await ctx.send(
        f"🃏 BLACKJACK\n"
        f"Bạn: {player}\nBot: {bot_hand}\n\n{result}"
    )

# ======================
# 🏆 TOP COIN
# ======================
@bot.command()
async def top(ctx):
    sorted_users = sorted(data.items(), key=lambda x: x[1]["coin"], reverse=True)

    text = "🏆 TOP COIN:\n\n"

    for i, (uid, info) in enumerate(sorted_users[:10]):
        try:
            user = await bot.fetch_user(int(uid))
            name = user.name
        except:
            name = "Unknown"

        text += f"{i+1}. {name} - {info['coin']} coin\n"

    await ctx.send(text)

# ======================
# 👑 OWNER SYSTEM
# ======================
@bot.command()
async def addcoin(ctx, member: discord.Member, amount: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ OWNER ONLY")

    uid = get_user(member.id)
    data[uid]["coin"] += amount
    save()

    await ctx.send(f"➕ +{amount} coin")

@bot.command()
async def removecoin(ctx, member: discord.Member, amount: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ OWNER ONLY")

    uid = get_user(member.id)
    data[uid]["coin"] -= amount
    save()

    await ctx.send(f"➖ -{amount} coin")

# ======================
# 🟢 SLASH (FIX 100% “did not respond”)
# ======================
@bot.tree.command(name="test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("SLASH OK ✔")

@bot.tree.command(name="purge")
@app_commands.checks.has_permissions(administrator=True)
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.response.defer()
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"🧹 Đã xoá {amount} tin nhắn")

@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(administrator=True)
async def ban(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    await member.ban()
    await interaction.followup.send(f"⛔ Ban {member.mention}")

@bot.tree.command(name="unban")
@app_commands.checks.has_permissions(administrator=True)
async def unban(interaction: discord.Interaction, user_id: str):
    await interaction.response.defer()
    user = await bot.fetch_user(int(user_id))
    await interaction.guild.unban(user)
    await interaction.followup.send(f"🔓 Unban {user.name}")

@bot.tree.command(name="timeout")
@app_commands.checks.has_permissions(administrator=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, seconds: int):
    await interaction.response.defer()
    until = discord.utils.utcnow() + discord.timedelta(seconds=seconds)
    await member.timeout(until)
    await interaction.followup.send(f"⏱ Timeout {member.mention}")

@bot.tree.command(name="untimeout")
@app_commands.checks.has_permissions(administrator=True)
async def untimeout(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    await member.timeout(None)
    await interaction.followup.send(f"🔓 Untimeout {member.mention}")

# ======================
# RUN BOT
# ======================
bot.run("MTUxNjM2MTM0Mjk5NzQ5OTk1Ng.G2WHS1.AOSnChp_Wjr91JX-cuKOI6cHbXMI6eLYg6gYqg")
