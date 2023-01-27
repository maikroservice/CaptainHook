from dotenv import load_dotenv
import discord
from discord import Intents
from discord.ext import commands
import os
import requests

load_dotenv()

# FIXME: TODO: we need to implement "!startlab or !startall"
# TODO: implement VPN file generation/QR code
# TODO: whisper/private message person requesting
# TODO: refactor prettify function to use client.command() and context

DIGITALOCEAN_TOKEN = os.getenv("DIGITALOCEAN_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD = os.getenv("DISCORD_GUILD")
#DISCORD_ALLOWED_ROLE_ID = os.environ.get("DISCORD_ALLOWED_ROLE_ID")

"""
twilio_token = os.environ.get("twilio_token")
twilio_account = os.environ.get("twilio_account")
twilio_phone_number = os.environ.get("twilio_phone_number")
user_phone_number = os.environ.get("user_phone_number")
"""
intents = Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def prettify_droplet_list_output(droplet_dict):
    embed = discord.Embed(
        title="🧪📦 BlueTeam Lab Status 🧪📦",
        url="https://pwnandprotect.com/",
        description="Red/Blue/Purple Team Labs",
        color=discord.Color.blue())

    for droplet in droplet_dict['droplets']:
        
        d_id = droplet['id']
        d_name = droplet['name']
        d_location = droplet['region']['name'] 
        d_status = droplet['status']
        d_networks = droplet['networks']
        d_ext_ip = d_networks["v4"][1]['ip_address']
        d_int_ip = d_networks["v4"][0]['ip_address']

        embed.add_field(name=f"{'🟢' if d_status == 'active' else '🟥'} **{d_name}**", value="", inline=False)
        embed.add_field(name="", value=f"🏠 ext: `{d_ext_ip}`, int: `{d_int_ip}`", inline=False)
        embed.add_field(name=f"{f'▶️ `!start {d_id}`' if d_status != 'active' else f'⏹️ `!stop {d_id}`'}", value="", inline=False)
        embed.add_field(name=f"{f'♻️ `!reboot {d_id}`' if d_status == 'active' else ''}", value="", inline=False)
    embed.set_footer(text="Lab by @kazmsec + @maikroservice")

    #embed.set_author(name="RealDrewData", url="", icon_url="")
    #embed.set_author(name=ctx.author.display_name, url="", icon_url=ctx.author.avatar_url)
    #embed.set_thumbnail(url="")
    """
    embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
    embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
    embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
    embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
    embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
    embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
    embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
    embed.set_footer(text="Learn more here: ")
    """

    return embed

def cmd_digitalocean(cmd, droplet_id):
    data = {"type": cmd}
    endpoint = f'https://api.digitalocean.com/v2/droplets/{droplet_id}/actions'
    headers = {"Authorization": f"Bearer {DIGITALOCEAN_TOKEN}"}
    response = requests.post(endpoint, data=data, headers=headers)
    return response.status_code

def list_droplets():
    endpoint = f'https://api.digitalocean.com/v2/droplets?page=1&per_page=10'
    headers = {"Authorization": f"Bearer {DIGITALOCEAN_TOKEN}", "Content-Type": "application/json"}
    response = requests.get(endpoint, headers=headers)
    if (response.status_code == 200):
        return response.json()
    else:
        return response.status_code

@client.event
async def on_message(message):
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
        
client.run(DISCORD_TOKEN)