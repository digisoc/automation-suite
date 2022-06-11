# DigiSoc Automation Suite

Automation tools designed by Andrew Xie (2021) to improve internal workflow for UNSW Digital Society (DigiSoc).

Two main tools have been written to achieve this:

- [Google Forms to Discord](https://github.com/axieax/google-forms-to-discord)

  - We use a [modified version](forms-to-discord/digisoc.js) of my [general script](https://github.com/axieax/google-forms-to-discord) to add additional functionality for automating generation of registration and attendance forms (with Google Sheets for analytics)
  - Updates to the general script should be merged into the modified script to ensure latest functionalities and bug fixes
  - **NOTE:** Please make sure to never commit secrets such as the Drive ID for the Google Drives folder, as well as the Discord Webhook URL

- [DigiBot (Discord Bot)](src/digibot)

## Workflow Diagrams

### Event Thread Automation Workflow

![Event Thread Workflow](assets/event_thread_workflow.png)

### Marketing Schedule Notifier Automation Workflow

![Marketing Schedule Workflow](assets/marketing_schedule_workflow.png)

## Setup

### Discord Server Setup for Google Forms to Discord

## Webhook Setup:
For setting up the channels to work with DigiBot:
* Ensure that the Manage Webhooks permission has been enabled in the server required
* Go to Server settings, under Integrations, click on Webhooks and then Create Webhook 
* Click on the channel you would like automated responses to be sent to
* Copy the webhook URL
* Copy the drive ID by copying the link on the required google drive folder
https://drive.google.com/drive/folders/{drive_id}?usp=sharing 
* Update both the form Google App Script and digisoc.js by changing the constants of webhook URL and drive IDs
  * In the code for the file digisoc.js, paste the Webhook URL between the '' symbols on for const webhookURL and driveID
* Ensure the file is saved

For further clarification, refer to https://github.com/axieax/google-forms-to-discord

### DigiBot

### To setup DigiBot on your Discord server:
* Go to the Discord Developer Portal 
https://discord.com/developers/applications 
* Create a new application and name it accordingly
* Click on Bot to create a bot, copy the bot token (required for local setup) 
* Set your bot to have admin permissions, with integer 8
* Select the following Privileged Gateway Intents: 
  * Server Members Intent, Message Content Intent (enable through GUI)
* Invite the bot to your server by using the URL generator under OAuth2 that will have a similar form to: 
`https://discord.com/api/oauth2/authorize?client_id={client_id}}&permissions=8&scope=bot`

### Setting up the Bot locally:
* Copy the ssh key of the automation-suite repository
* On the terminal write:
`code .env`
* Save your Discord bot token in the .env file in the following format: 
`TOKEN=DISCORD_BOT_TOKEN`
* To start DigiBot, type the following on the terminal:
`python3 main.py`
For further reading into permissions relating to coded intents on members: 
https://discordpy.readthedocs.io/en/latest/api.html#discord.Intents.members

### Docker Deployment

Build image
`docker build -t digibot-image .`

Create container from image
`docker run digibot-image`
add `-d` flag for daemonised/detached process (in background)

## Ensuring the discord server is compatible with DigiBot
Initial discord server preparation:
* Create a category with a channel called requests and a channel called archives
  * Note that the event name index for event name is zero-indexed