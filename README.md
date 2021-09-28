# DigiSoc Automation Suite

Automation tools designed by Andrew Xie (2021) to improve internal workflow for UNSW Digital Society (DigiSoc).

Two main tools have been written to achieve this:

- [Google Forms to Discord](https://github.com/axieax/google-forms-to-discord)

  - We use a [modified version](forms-to-discord/digisoc.js) of this script to add additional functionality for automating generation of registration and attendance forms (with Google Sheets for analytics)
  - **NOTE:** Please make sure to never commit secrets such as the Drive ID for the Google Drives folder, as well as the Discord Webhook URL

- [DigiBot (Discord Bot)](src/digibot)

## Workflow Diagrams

### Event Thread Automation Workflow

![Event Thread Workflow](assets/event_thread_workflow.png)

### Marketing Schedule Notifier Automation Workflow

![Marketing Schedule Workflow](assets/marketing_schedule_workflow.png)

## Setup

### Discord Server

Webhook, requests channel, archives channel, events category, permissions, role names

### DigiBot

Put your Discord bot token in a .env file

This can be found in https://discord.com/applications/{application_id}/bot

`TOKEN=DISCORD_BOT_TOKEN`

### Docker Deployment

Build image
`docker build -t digibot-image .`

Create container from image
`docker run digibot-image`
add `-d` flag for daemonised/detached process (in background)
