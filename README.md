# DigiSoc Automation Suite for Internal Workflow

Andrew Xie, 2021

Description

## Setup

### Auth

Put your Discord bot token in a .env file

This can be found in https://discord.com/applications/{application_id}/bot

`TOKEN=DISCORD_BOT_TOKEN`

### Docker

Build image
`docker build -t digibot-image .`

Create container from image
`docker run digibot-image`
add `-d` flag for daemonised/detached process (in background)

### Google Forms to Discord

### Discord event thread automation (DigiBot)
