import discord
from discord.ext import commands
import random
import json
import os

# ======================
# INTENTS
# ======================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="N!", intents=intents)

# ======================
# DATABASE
# ======================
DATA_FILE = "money.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user(data, user_id):
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = 1000  # tiền khởi đầu
    return user_id

# ======================
# BOT READY
# ======================
@bot.event
async def on_ready():
    print(f"NightBot đã đăng nhập: {bot.user}")

# ======================
# PING
# ======================
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

# ======================
# XEM TIỀN
# ======================
@bot.command()
async def coin(ctx):
    data = load_data()
    user = str(ctx.author.id)

    if user not in data:
        data[user] = 1000

    save_data(data)
    await ctx.send(f"💰 Bạn có {data[user]} coin")

# ======================
# DAILY
# ======================
@bot.command()
async def daily(ctx):
    data = load_data()
    user = str(ctx.author.id)

    if user not in data:
        data[user] = 1000

    reward = random.randint(200, 800)
    data[user] += reward

    save_data(data)
    await ctx.send(f"🎁 Bạn nhận {reward} coin!")

# ======================
# CF (CƯỢC TUNG XU)
# ======================
@bot.command()
async def cf(ctx, bet: int):
    data = load_data()
    user = str(ctx.author.id)

    if user not in data:
        data[user] = 1000

    if bet <= 0:
        return await ctx.send("❌ Số tiền không hợp lệ!")

    if bet > data[user]:
        return await ctx.send("❌ Không đủ coin!")

    result = random.choice(["win", "lose"])

    if result == "win":
        data[user] += bet
        text = f"🪙 Thắng +{bet} coin!"
    else:
        data[user] -= bet
        text = f"💥 Thua -{bet} coin!"

    save_data(data)
    await ctx.send(f"🎲 CF: {text}")

# ======================
# BJ (XÌ DÁCH CƯỢC)
# ======================
@bot.command()
async def bj(ctx, bet: int):
    data = load_data()
    user = str(ctx.author.id)

    if user not in data:
        data[user] = 1000

    if bet <= 0:
        return await ctx.send("❌ Số tiền không hợp lệ!")

    if bet > data[user]:
        return await ctx.send("❌ Không đủ coin!")

    player = random.randint(15, 22)
    dealer = random.randint(15, 22)

    if player > 21:
        result = "lose"
    elif dealer > 21 or player > dealer:
        result = "win"
    elif player == dealer:
        result = "draw"
    else:
        result = "lose"

    if result == "win":
        data[user] += bet
        text = f"🎉 Thắng +{bet} coin!"
    elif result == "lose":
        data[user] -= bet
        text = f"💥 Thua -{bet} coin!"
    else:
        text = "🤝 Hòa!"

    save_data(data)

    await ctx.send(
        f"🃏 BJ\n"
        f"Bạn: {player}\n"
        f"Dealer: {dealer}\n\n"
        f"{text}"
    )

# ======================
# RUN BOT
# ======================
bot.run("MTUxNjM2MTM0Mjk5NzQ5OTk1Ng.GT79Mp.21r54tNkU2ac20yT51s4iosT4XadEj4EOiQ8_I")
