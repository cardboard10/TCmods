execute at @s[scores={class=6}] if block ~ ~ ~ minecraft:water run attribute @s minecraft:movement_speed base set .3
execute at @s[scores={class=6}] if block ~ ~ ~ minecraft:water run scoreboard players set @s inwater 1
execute at @s[scores={class=6}] if block ~ ~ ~ #minecraft:air run attribute @s minecraft:movement_speed base set .05
execute at @s[scores={class=6}] if block ~ ~ ~ #minecraft:air run scoreboard players set @s inwater 0