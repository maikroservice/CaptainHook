from dotenv import load_dotenv
import discord
from discord import Intents
from discord.ext import commands
from discord.utils import get
import os
from verify_gumroad import verify_gumroad_license
from digital_ocean import *

load_dotenv()

DIGITALOCEAN_TOKEN = os.getenv("DIGITALOCEAN_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD = os.getenv("DISCORD_GUILD")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
GUMROAD_PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")
DISCORD_SOC101_ROLE_ID = int(os.getenv("DISCORD_SOC101_ROLE_ID"))
#DISCORD_ALLOWED_ROLE_ID = os.environ.get("DISCORD_ALLOWED_ROLE_ID")

intents = Intents.default()
intents.message_content = True
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)
guild = bot.get_guild(DISCORD_GUILD_ID)


@bot.event
async def on_ready():
    print("I am running on " + bot.user.name)
    print("With the ID: " + str(bot.user.id))
    print('Bot is ready to be used')
   # after it is ready do it

    takenGuild = bot.get_guild(DISCORD_GUILD_ID)
    print(takenGuild.id)

    for g in bot.guilds:
        print(g)
        print(g.id)
        for role in guild.roles:
            if role == "SOC Analyst 101":
                print(role, role.id)


@bot.event
#@bot.command(pass_context=True)
async def on_message(message):

    if message.content.startswith('!verify'):
        _, gumroad_key = message.content.split(" ")
        gumroad_key_verified = verify_gumroad_license(gumroad_key)
        
        
        if gumroad_key_verified:
            #role = get(message.server.roles, name='SOC Analyst 101')
            soc101 = await guild.get_role(DISCORD_SOC101_ROLE_ID) 
            await bot.add_roles(message.author, soc101)

            # https://docs.replit.com/tutorials/python/discord-role-bot
        # add user to SOC Analyst 101 Discord Group
        # TODO: read "group" from verification product
            

            #roles = [discord.utils.get(server.roles)]

            #member = await server.fetch_member(message.author.id)
            


        await message.channel.send(f'`Verification - {gumroad_key_verified}` ')

    if message.content.startswith('!reboot'):
        _, droplet_id = message.content.split(" ")
        statuscode = cmd_digitalocean('reboot', droplet_id)
        await message.channel.send(f'`HTTP{statuscode} - rebooting box {droplet_id}...`')

    elif message.content.startswith('!start'):
        _, droplet_id = message.content.split(" ")
        statuscode = cmd_digitalocean('power_on', droplet_id)
        await message.channel.send(f'`HTTP{statuscode} - starting box {droplet_id}...`')
    
    elif message.content.startswith('!stop'):
        _, droplet_id = message.content.split(" ")
        statuscode = cmd_digitalocean('shutdown', droplet_id)
        await message.channel.send(f'`{statuscode} - attempting graceful shutdown of box {droplet_id}...`')

    elif message.content.startswith('!ping'):
        author_role_ids = [y.id for y in message.author.roles]
        if int(discord_allowed_role_id) in author_role_ids:
            sms_message = text_message()
            await message.channel.send(
                f'Texting Invictus. Message status: {sms_message}' # Customize to your name
            )  
    elif message.content.startswith('!test'):
        author_role_ids = [y.id for y in message.author.roles]
        if int(discord_allowed_role_id) in author_role_ids:
            await message.channel.send('I am awake...')

    elif message.content.startswith('!list'):
        droplet_dict = list_droplets()
        
        droplet_message = prettify_droplet_list_output(droplet_dict)
        await message.channel.send(embed=droplet_message)
        
bot.run(DISCORD_TOKEN)