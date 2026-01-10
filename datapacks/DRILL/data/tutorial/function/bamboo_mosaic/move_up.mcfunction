execute as @n[type=minecraft:item_display] at @s run clone ^ ^ ^ ^ ^ ^ ^ ^1 ^
execute as @n[type=minecraft:item_display] at @s run tp @s ^ ^1 ^
execute as @n[type=minecraft:item_display] at @s run setblock ^ ^-1 ^ air
tp @n[type=interaction,tag=block_detector] @s

