# ISU Dining Bot

ISU Dining Bot is an interface for the dining centers at Iowa State University through discord. Through the discord bot, you can search menus for breakfast, lunch, and dinner, as well as search for certain foods.

## Required Libraries:
  1. Python
  2. discord.py
  3. dotenv
  4. urllib
  5. json
  6. ssl
  7. asyncio

## Commands:

```!udcc``` - Check menu of Union Drive Marketplace, optional [time].
> Usage: `!udcc [time]`

```!windows``` - Check menu of Friley Windows, optional [time].
> Usage: `!windows [time]`

```!seasons``` - Check menu of Seasons Marketplace, optional [time].
> Usage: `!seasons [time]`

```!search``` - Returns location of [food] if found, optional [time].
> Usage: `!seasons "[substring]" [time]`

> Aliases: `!tendies`, `!wingies`, `!nuggies`,

```!reload``` - Reloads the menu for all dining centers.

```!help``` - Returns link for commands, and invite link.