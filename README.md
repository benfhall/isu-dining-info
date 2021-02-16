# isu-dining-info
discord bot and script to get meals from UDCC and Windows.

required libraries: 

    - discord.py   
    - numpy
    - python-dotenv

Commands:

    - ![building] [time]      :   find the menu for given [time] at given [building].
    - !search [term] [time]   :   searches for [term] at all dining centers, given [time].
    - !tendies [time] :   searches for tender, [time] is optional.
    - !nuggies [time] :   searches for nugget, [time] is optional.
    - !wingies [time]   :   searches for wing, [time] is optional.
    - !upvote [food]    :   upvotes [food].
    - !downvote [food]  :   downvotes [food].
    - !reload         :   reloads the menu.
    - !help           :   displays options and usage of commands.


Arguments:
    
    - [building]  :   udcc/windows/seasons
    - [time]      :   breakfast/lunch/dinner (breakfast not available for Windows)
    - [term]      :   any food
