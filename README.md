# DigiSoc Automation Suite

Automation tools designed by Andrew Xie (2021) to improve DigiSoc internal workflow.

Two main tools:

- [Google Forms to Discord](https://github.com/axieax/google-forms-to-discord)
- [DigiBot (Discord Bot)](src/digibot)

## Workflow Diagrams

### Event Thread Automation Workflow

![Event Thread Workflow](assets/event_thread_workflow.png)

### Marketing Schedule Notifier Automation Workflow

![Marketing Schedule Workflow](assets/marketing_schedule_workflow.png)

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
