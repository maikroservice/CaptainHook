# Reboot Your DigitalOcean Droplet from Discord
You can use this bot to interact with your DigitalOcean droplets from Discord.

My Cloud Labs are hosted on DigitalOcean and we are building a bot so that users can self-service their labs and reset the environments when need be.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## Commands
`!start <droplet_id>`: starts the droplet with the ID droplet_id.
`!stop <droplet_id>`: attempts graceful shutdown of the droplet with the ID droplet_id.
`!reboot <droplet_id>`: attempts rebooting the droplet with the ID droplet_id.
`!test`: Checks whether the bot is responsive.

## Environmental Variables You Need to Setup
1. `DIGITALOCEAN_TOKEN`: Find this in your DigitalOcean account. Click APIs and generate an API key.
2. `DISCORD_TOKEN`: This is the bot's discord token. Find it in your discord account.
3. `DISCORD_ALLOWED_ROLE_ID`: This is the role of Discord users who can command the bot. Find it in Discord Server Settings -> Roles. Copy the role id. <NOT IMPLEMENTED YET>
4. `DISCORD_GUILD`: The ID of the Discord Server you want to connect to.

## TODO
- implement startall / stopall function
- implement forcedshutdown
- implement vpn generation command?
- implement copying of the whole stack for individuals
- hard reset option (in case a user bricked something)