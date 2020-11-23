# This example requires the 'members' privileged intents

import discord
import asyncio
from discord.ext import commands
import os
import random
import json
import requests
from dotenv import load_dotenv
from twitter import get_random_tweet

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
    """Rolls a dice in NdN format.

    Example: !roll 2d20
    """
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


@bot.command()
async def twitter(ctx, username: str):
    """Get a random tweet from the last 20 tweets of a specified account"""
    try:
        tweet = get_random_tweet(username)
        await ctx.send(tweet)
    except:
        await ctx.send('Twitter User Not Found')


@bot.command()
async def poll(ctx, question: str, *choices: str):
    """Start a poll with a specified question and a list of choices"""
    print(ctx.author.mention)
    if len(choices) > 8:
        return await ctx.send('Sorry, maximum 8 options allowed')
    options = []
    emoji_options = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
    for choice in choices:
        options.append(f"{emoji_options[len(options)]}. {choice}")
    lines = [f"New Poll From {ctx.author.mention}:", f"**{question}**"] + options
    response = '\n'.join(lines)
    message = await ctx.send(response)

    for count in range(len(choices)):
        await message.add_reaction(emoji_options[count])


bot.run(os.environ.get('DISCORD_KEY'))