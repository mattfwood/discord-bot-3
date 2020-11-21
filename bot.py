# This example requires the 'members' privileged intents

import discord
import asyncio
from discord.ext import commands
import os
import random
import json
import requests
from dotenv import load_dotenv

load_dotenv()


description = '''Mongoose Bot, Beware'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def subreddit(ctx, user_input: str):
    """Get a random item from the top 20 items on a subreddit"""
    try:
        res = requests.get(
            f'https://www.reddit.com/r/{user_input}/hot.json?limit=20',
            headers={'User-agent': 'Bone-Bot-Discord'},
        )
        json = res.json()
        random_post = random.choice(json['data']['children'])['data']
        # random_url = random.choice(json['data']['children'])['data']['url']
        await ctx.send(f"{random_post['title']} \n {random_post['url']}")
    except IndexError:
        await ctx.send('Subreddit not found')


bot.run(os.getenv('DISCORD_TOKEN'))