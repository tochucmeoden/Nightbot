import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os
import asyncio

# ======================
# INTENTS
# ======================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ======================
# BOT CLASS (SLASH SUPPORT)
# ======================
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="N!", intents=intents)
        self.tree = app_commands.CommandTree(self)

bot = MyBot()

# ======================
# OWNER BOT
# ======================
OWNER_ID = 1301466547209895960

def is_owner(interaction):
    return interaction.user.id == OWNER_ID

# ======================
# DATA SYSTEM
# ======================
FILE = "data.json"

def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load()

def get_user(uid):
    uid = str(uid)
    if uid not in data:
        data[uid] = {"coin": 1000}
    return uid

# ======================
# READY
# ======================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot online: {bot.user}")

# ======================
# 🎮 COIN SYSTEM (PREFIX)
# ======================
@bot.command()
async def coin(ctx):
    uid = get_user(ctx.author.id)
    await ctx.send(f"💰 {data[uid]['coin']} coin")

@bot.command()
async def daily(ctx):
    uid = get_user(ctx.author.id)
    reward = random.randint(200, 600)
    data[uid]["coin"] += reward
    save()
    await ctx.send(f"🎁 +{reward} coin")

# ======================
# 🪙 COIN FLIP
# ======================
@bot.command()
async def cf(ctx, bet: int, choice: str):
    uid = get_user(ctx.author.id)
    choice = choice.lower()

    if choice not in ["head", "tail"]:
        return await ctx.send("❌ N!cf 100 head")

    if data[uid]["coin"] < bet:
        return await ctx.send("❌ Không đủ coin")

    msg = await ctx.send("🪙 Tung đồng xu...")

    await asyncio.sleep(2)

    result = random.choice(["head", "tail"])
    emoji = "🟡 HEAD" if result == "head" else "🔵 TAIL"

    if choice == result:
        data[uid]["coin"] += bet
        text = f"🎉 +{bet}"
    else:
        data[uid]["coin"] -= bet
        text = f"💥 -{bet}"

    save()

    await msg.edit(content=f"🪙 KẾT QUẢ: {emoji}\n{text}")

# ======================
# 🃏 BLACKJACK SIMPLE
# ======================
@bot.command()
async def bj(ctx, bet: int):
    uid = get_user(ctx.author.id)

    if data[uid]["coin"] < bet:
        return await ctx.send("❌ Không đủ coin")

    p = random.randint(12, 22)
    b = random.randint(12, 22)

    if p > 21:
        res = "lose"
    elif b > 21 or p > b:
        res = "win"
    elif p == b:
        res = "draw"
    else:
        res = "lose"

    if res == "win":
        data[uid]["coin"] += bet
        text = f"🎉 +{bet}"
    elif res == "lose":
        data[uid]["coin"] -= bet
        text = f"💥 -{bet}"
    else:
        text = "🤝 Hòa"

    save()
    await ctx.send(f"🃏 Bạn: {p} | Bot: {b}\n{text}")

# ======================
# 👑 OWNER BOT COMMANDS
# ======================
@bot.command()
async def addcoin(ctx, member: discord.Member, amount: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ Chỉ OWNER BOT")

    uid = get_user(member.id)
    data[uid]["coin"] += amount
    save()
    await ctx.send(f"➕ +{amount} coin")

@bot.command()
async def removecoin(ctx, member: discord.Member, amount: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ Chỉ OWNER BOT")

    uid = get_user(member.id)
    data[uid]["coin"] -= amount
    save()
    await ctx.send(f"➖ -{amount} coin")

# ======================
# 🧹 SLASH /purge
# ======================
@bot.tree.command(name="purge", description="Xóa tin nhắn")
@app_commands.checks.has_permissions(administrator=True)
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"🧹 Xóa {amount} tin nhắn", ephemeral=True)

# ======================
# ⛔ SLASH /ban
# ======================
@bot.tree.command(name="ban", description="Ban người dùng")
@app_commands.checks.has_permissions(administrator=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"⛔ Ban {member}")

# ======================
# ⏱ SLASH /timeout
# ======================
@bot.tree.command(name="timeout", description="Timeout user")
@app_commands.checks.has_permissions(administrator=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, seconds: int):
    await member.timeout(discord.utils.utcnow() + discord.timedelta(seconds=seconds))
    await interaction.response.send_message(f"⏱ Timeout {member} {seconds}s")

# ======================
# RUN BOT
# ======================
bot.run("MTUxNjM2MTM0Mjk5NzQ5OTk1Ng.GzDHOw.kz0GXnvx5-_xKYfHWQyWNRh_NoBToXQIRgV-PU")
