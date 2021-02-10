# DigiSoc Event Request Automation
This Discord bot automates [Google Form to Discord Webhook Notifications](https://github.com/axieax/google-forms-to-discord), designed for the DigiSoc internal team to solve communication issues with workflow.

Features:
- Create a new text channel for each new incoming request in the `#requests` channel, visible to relevant portfolios with permissions setup appropriately
- Ability to `!redo` reply a request from the #requests channel to manually complete the above (in case of bot downtime)
- Channel archival function `!archive` which archives channel content into a txt file (posted to #requests) before deleting the channel itself

Required Discord bot permissions:
- Administrator (in order to add the 'Manage Permissions' permission to certain users)

General Setup:
1. Setup the bot under Discord Developer Portal \> Applications and invite to your Discord server
1. Add your bot token to a .env file as an environment variable (aka TOKEN=...)
1. Create a category `🍺-Events` with a `#requests` text channel inside it (text channel hidden by default)
1. Setup a [Google Form to Discord Webhook](https://github.com/axieax/google-forms-to-discord) in `#requests`, linked to the DigiSoc Marketing Request Form
