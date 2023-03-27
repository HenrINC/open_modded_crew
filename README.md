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

- **Crew Management**: The bot allows users to create, manage, and customize their own crews within the Social Club platform. Users can invite members to their crews, assign roles, and manage crew settings.

- **Communication**: Users can communicate with their crew members using the bot's messaging features.

## Commands

The bot provides a set of commands that allow users to interact with it and access its functionality. By default, only the `/command` and `/service` commands are enabled. The `/command` command is used to manage, enable, or disable other commands, while the `/service` command is used to manage services that the bot can provide. In this section, we will provide a description of each command and how to use them. Additionally, we will show how to add new commands to the bot.

## Conclusion

Open_modded_crew is a powerful tool for managing crews and communicating with crew members within the Rockstar Games Social Club platform. With its intuitive interface and powerful features, it makes it easy for gamers to stay connected with their crew members and organize their gaming communities.