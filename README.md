# Open Modded Crew Bot

Open_Modded_Crew is a Python-based tool that provides Discord-like functionality for the Rockstar Games Social Club (RGSC). It allows you to manage your crew(s) on RGSC in a more efficient and user-friendly way, with features such as member management, enhanced customization, and crew statistics.

Unlike Discord bots, Open_Modded_Crew is not a Discord bot itself. Instead, it is designed to work exclusively with RGSC, providing Discord-like functionality within the RGSC environment. This means that you can use Open_Modded_Crew to manage your crew(s) directly on RGSC, without the need to switch to a different platform.

With Open_Modded_Crew, you can communicate with your crew members, create custom events, view crew statistics, and much more. Whether you're a crew leader or member, Open_Modded_Crew is a useful tool that can help you manage your RGSC crew(s) more efficiently.

## Getting Started

To use the open_modded_crew bot, you'll need to follow these steps:

1. Clone the repository from the open_modded_crew GitHub page.

2. Create a `credentials.json` file in the same directory as `open_modded_crew.py` with your Social Club email and password in the following format:
`
{
    "email": "address@server",
    "password": "password"
}
`
3. Create a `config.json` file in the same directory as `open_modded_crew.py` with the names of the crews you want to manage in the following format:
`
{
    "crews": [
        "crew_name_1",
        "crew_name_2"
    ]
}
`
4. Install the required dependencies using the `pip install -r requirements.txt` command.

5. Start the bot by running the `open_modded_crew.py` script.

## Features

The open_modded_crew bot includes the following features:

- **Crew Management**: The bot allows users to create, manage, and customize their own crews within the Social Club platform.

- **Communication**: Users can communicate with their crew members using the bot's messaging features.

- **Rockstar Games Social Club API integration:** The bot seamlessly integrates with the Rockstar Games Social Club API, providing real-time updates on crew and player information.

- **Customizable commands and services:** The bot's command and service system is highly customizable, allowing you to add, remove, and modify commands and services to suit your specific needs.

- **Automatic moderation using AI:** The bot includes an automatic moderation service that uses AI to detect and flag inappropriate or offensive content in chat.

- **Translation translation using AI:** The bot uses AI to automatically detect the source language of messages on the crew wall and translate them to a specified language, making it easier for members who speak different languages to communicate and stay engaged with the crew.

## Commands

The bot provides a set of commands with a CLI-like syntax that allow users to interact with it and access its functionality. By default, only the `/command` and `/service` commands are enabled. The `/command` command is used to manage, enable, or disable other commands, while the `/service` command is used to manage services that the bot can provide. In this section, we will provide a description of each command and how to use them.

### Rank Requirements 

Each command has a rank requirement, which is based on the RGSC rank system. In this system, the leader (highest rank) is given a rank of 0, the commissioner has a rank of 1, and so on, until the muscle rank, which is 4. 

To restrict access to a command based on rank, you can set a minimum rank requirement for the command. For example, if you set the rank requirement to 2, only members with a rank of 2 or higher (which includes lieutenants and above) will be able to use the command. 

To set the rank requirement for a command, use the `--rank` option on either the `-update` or the `-add` switch of the `/command` command

Example: `/command -update style --rank 2` will make the `/style` command available for lieutenants an higher

### Using the /command command

You can use the following switches with the `/command` command:

- `-add <command name> [--rank <minimum rank>]`: Adds a new command with the specified name.
- `-remove <command name> [--rank <minimum rank>]`: Removes a command with the specified name.
- `-update <command name> [--rank <minimum rank>]`: Updates the configuration of the command with the specified name.
- `-list`: Lists all added commands.
- `-reload`: Commits and applies any changes made to the command configuration.

### Using the /service command

You can use the following switches with the `/service` command:

- `-add <service name>`: Adds a new service with the specified name.
- `-remove <service name>`: Removes a service with the specified name.
- `-update <service name>`: Updates the configuration of the service with the specified name.
- `-list`: Lists all added service.
- `-reload`: Commits and applies any changes made to the service configuration.

## Builtin Commands and Services

The bot also comes with some builtin commands and services that can be enabled with `/command -add` and `/service -add` commands. By default, these features are not enabled and must be added manually.

### Commands

Here is a list of the builtin commands that can be added:

- `/joke`: Returns a random joke from the [official JokeAPI](https://jokeapi.dev/).
- `/mute` (PLANNED): Removes all messages posted by a specific player. The player can still post but all of it's messages will be removed every 5 seconds
- `/event` (PLANNED): Plans events at a certain date and posts reminders on the wall before the event starts
- `/coinflip`: Flips a coin and returns either "heads" or "tails".
- `/roll [-max <number>]`: Rolls a dice with a specified number of sides (default is 6) and returns the result.
- `/style`(NEED UPDATE): Allows enhanced crew customization (more on that in the "style" section).

### Services

Here is a list of the builtin services that can be added:

- `auto-moderation`: Automatically moderates messages using the "unitary/toxic-bert" model. More info in the "Auto-moderation" section
- `welcome-message`(NEED TO PORT FROM LEGACY): Sends a welcome message to new members when they join the server.
- `leave-message`(PLANNED): Sends a message to the server when a member leaves.
- `translator`: Comments posts with it's translation in configured languages
- `archive`: Only keeps only the commands posted less than 10 minutes ago to keep the crew wall clean.
- `tracking`: Allows you to track the invitations sent by your crew members. How much were sent, how much were accepted, how much the invitee stayed in the crew.  
- `style`(NEED UPDATE): Allows enhanced crew customization (more on that in the "style" section).

To enable a builtin command or service, use the `/command -add` or `/service -add` command with the name of the command or service you want to enable. For example, to enable the `/joke` command, use `/command -add joke`.

## Style

__Rockstar changed the EditCrew endpoint, styles won't apply on your crew, i'm working on a fix__ 

This whole project started as warper around the "EditCrew" API endpoint so the style and modding aspect of the project is still there in the form of a service and a command. The service is there to commit style config every 2 minutes to avoid unnecessary requests. The command is there to update the style config.

By default, the style command and service are not enabled. To enable them, use the `/command -add style` and `/service -add style` commands.

You will interact with the style service using the `/style` command of which you can read the documentation below

- `-get [--property <property name>]`: Get the style configuration. If `--property` is specified, only gets the value of the specified property.
- `-set [--property <property name> [--value <property value>]]`: Set the style configuration. If `--property` is defined, only sets the value of the specified property. If `--value` is specified, sets it to the specified value, else to the value of the current property.
- `-add [--property <property name> [--value <property value>]]`: Add a new value the style configuration. If `--property` is defined, only sets the value of the specified property. If `--value` is specified, sets it to the specified value, else to the value of the current property. All properties can have multiple values. The service will randomly choose one from the list of values when committing the changes. 
- `-remove --property <property name> --value <property value>`: Remove a value's property from the configuration.

## Auto-moderation

The Auto-Moderator service is designed to help manage the crew by automatically moderating messages using an AI model. This service is not enabled by default, and needs to be activated using the `/service -add auto-moderator` command.

Note that while the Auto-Moderator service can help reduce the workload of moderators, it is not perfect and may occasionally make mistakes. Therefore, it is important to continue to manually moderate the crew to ensure that it remains a safe and welcoming community.

## Conclusion

Open_modded_crew is a powerful tool for managing crews and communicating with crew members within the Rockstar Games Social Club platform. With its intuitive interface and powerful features, it makes it easy for gamers to stay connected with their crew members and organize their gaming communities.