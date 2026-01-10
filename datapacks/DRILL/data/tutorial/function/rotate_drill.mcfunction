scoreboard objectives add drill_dir dummy


# 1. Target the nearest drill and increment its rotation score
execute as @n[type=item_display] run scoreboard players add @s drill_dir 1

# 2. Reset the score to 0 if it goes past 5 (the last direction)
execute as @e[tag=tutorial.custom_block, scores={drill_dir=6..}] run scoreboard players set @s drill_dir 0

# 3. Apply the Facing NBT based on the score
execute as @e[tag=tutorial.custom_block, scores={drill_dir=0}] at @s run function tutorial:bamboo_mosaic/look_down
execute as @e[tag=tutorial.custom_block, scores={drill_dir=1}] at @s run function tutorial:bamboo_mosaic/look_up
execute as @e[tag=tutorial.custom_block, scores={drill_dir=2}] at @s run function tutorial:bamboo_mosaic/look_north
execute as @e[tag=tutorial.custom_block, scores={drill_dir=3}] at @s run function tutorial:bamboo_mosaic/look_south
execute as @e[tag=tutorial.custom_block, scores={drill_dir=4}] at @s run function tutorial:bamboo_mosaic/look_west
execute as @e[tag=tutorial.custom_block, scores={drill_dir=5}] at @s run function tutorial:bamboo_mosaic/look_east
