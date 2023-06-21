from dotenv import load_dotenv
import discord
from discord import Intents
from discord.ext import commands
import os
from verify_gumroad import verify_gumroad_license
from digital_ocean import *
import logging
import sys

date_strftime_format = "%d-%b-%y %H:%M:%S"
message_format = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(format=message_format, 
                    datefmt=date_strftime_format, 
                    stream=sys.stdout)


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
intents.members = True

#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)
guild = bot.get_guild(DISCORD_GUILD_ID)


@bot.event
async def on_ready():
    logging.debug("I am running on " + bot.user.name)
    logging.debug("With the ID: " + str(bot.user.id))
    logging.debug('Bot is ready to be used')
   # after it is ready do it

    takenGuild = bot.get_guild(DISCORD_GUILD_ID)
    logging.debug(takenGuild.id)

    for g in bot.guilds:
        logging.debug(g)
        logging.debug(g.id)
        for role in g.roles:
            if role == "SOC Analyst 101":
                logging.debug(role, role.id)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.event
async def on_member_join(member):
    
    guild = bot.get_guild(DISCORD_GUILD_ID)
    member = await guild.fetch_member(member)
    message = f'Hi {member.name}, welcome to the Purple Team Hacking Club. If you bought the Practical SOC Analyst 101 course, you should be able to verify your License Key (get them here: https://app.gumroad.com/d/8dada12a842072e0e2bc3199cc0791bc at the very bottom, or click on Receipt -> View Receipt )  with a whisper to @CaptainHook using the following command: !verify <LICENSE_KEY_HERE> - once that is done you will gain access to a hidden course area and the practical-soc-analyst-101 channel'
    logging.debug(f"{member.name} joined -  {message}")
    await member.send(message)

@bot.command()
async def verify(ctx, gumroad_key: str):
    logging.info(f'{ctx.author} ({ctx.author.id}), tried to verify with {gumroad_key}')
    # if someone did not to remove the `<` or `>` from the key, we tell them to do so
    if gumroad_key.startswith("<") or gumroad_key.endswith(">"):
        gumroad_key_verified = {"verification":False, 
                                "message":"You need to remove the `< and >` from your message"}
    else:
        gumroad_key_verified = verify_gumroad_license(GUMROAD_PRODUCT_ID, gumroad_key)
        
        
    if gumroad_key_verified["verification"] == True:
        #role = get(message.server.roles, name='SOC Analyst 101')
        guild = bot.get_guild(DISCORD_GUILD_ID)
        soc101 = guild.get_role(DISCORD_SOC101_ROLE_ID)
        member = await guild.fetch_member(ctx.author.id)

        await member.add_roles(soc101)
        # https://docs.replit.com/tutorials/python/discord-role-bot
        # add user to SOC Analyst 101 Discord Group
        # TODO: read "group" from verification product
        #roles = [discord.utils.get(server.roles)]
        #member = await server.fetch_member(message.author.id)

        # if all went well the verification is complete and we can share that with the user

    else:
        logging.info(gumroad_key_verified)
        
        await ctx.reply(f'Verification {gumroad_key_verified["verification"]} - {gumroad_key_verified["message"]}')

@verify.error
async def verify_error(ctx, error):
    # https://stackoverflow.com/questions/67874947/how-to-check-if-required-argument-is-missing-in-discord-py
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.reply(f'Verification needs a key - use !verify <YOUR_KEY_HERE>')

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
        
bot.run(DISCORD_TOKEN)