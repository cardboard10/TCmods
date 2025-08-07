clear @s
function pvp:clear

#scoreboard players set @s deaths 0

execute as @s[scores={class=1}] run function pvp:startc1

execute as @s[scores={class=2}] run function pvp:startc2

execute as @s[scores={class=3}] run function pvp:startc3

execute as @s[scores={class=4}] run function pvp:startc4

execute as @s[scores={class=5}] run function pvp:startc5

execute as @s[scores={class=6}] run function pvp:startc6




