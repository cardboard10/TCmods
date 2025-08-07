
execute at @s[scores={usemace=5}] run execute at @e[limit=1,distance=1.5..,sort=nearest] run summon minecraft:lightning_bolt ~ ~ ~
execute as @s[scores={usemace=5}] run gamemode creative @s
execute as @s[scores={usemace=5}] run schedule function pvp:survival 1s
execute as @s[scores={usemace=5}] run scoreboard players set @s usemace 6

