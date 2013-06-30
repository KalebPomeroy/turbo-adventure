The application will have 3 separate sections

- Lobby
- Headquarters
- Battle

### Lobby
This is the default landing page for players. It will include
a global chat, logged in player list, current games, and other 
social information (including rankings). 

Actions from this page:
 - ~~Chat in lobby~~
 - ~~Host new game~~
 - Join hosted game (as participant or watcher)
 - Challenge player
 - ~~Goto Headquarters~~

### Headquarters
This is the user page. It includes current lists/configurations,
current win ratios, ability for replays, ect.
 - ~~Select and modify list~~
 - ~~Create new lists~~

### Battlefield
This is where the battles take place

Ships have Speed, Hull, and Shield

Turn Phases:
    - Select active ship
    - Move 0-[movement] spaces
        - Select destination (within range)
        - Ships can not rotate except after moving, and then only 90 degrees
        - Confirm Movement
    - Fire one weapon
        - Choose weapon
            - Each weapon has a cooldown of 3 turns 
            - Choose Target
        - Confirm
        - Resolve Damage
            - damage = [weapon.strength] - [target.shield]
            - shot_difficulty = ([actual_range] / [weapon.range]) / 10  -- (ie, 5/5 = 10%, 1/5= 2%)
            - evasion = ([target.speed] / 2) * [shot_difficulty]  (ie speed=6 - 30%, 6%)
            - If not evaded: [target.hull] - damage





### Unanswered questions
Why are players playing? What rewards are there?



