import requests
import os
import discord

DIGITALOCEAN_TOKEN = os.getenv("DIGITALOCEAN_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD = os.getenv("DISCORD_GUILD")


def prettify_droplet_list_output(droplet_dict):
    embed = discord.Embed(
        title="🧪📦 BlueTeam Lab Status 🧪📦",
        url="https://pwnandprotect.com/",
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
        embed.add_field(name="", value=f"🏠 ext: `{d_ext_ip}` int: `{d_int_ip}`", inline=False)
        embed.add_field(name=f"{f'▶️ `!start {d_id}`' if d_status != 'active' else f'⏹️ `!stop {d_id}`'}", value="", inline=False)
        embed.add_field(name=f"{f'♻️ `!reboot {d_id}`' if d_status == 'active' else ''}", value="", inline=False)
    embed.set_footer(text="Lab by @kazmmsec + @maikroservice")

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
