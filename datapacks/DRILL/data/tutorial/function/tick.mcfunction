
execute as @e[tag=tutorial.custom_block] at @s run function tutorial:as_blocks

recipe give @a tutorial:drill
recipe give @a tutorial:drill_rotator

scoreboard objectives add drill_dir dummy

execute as @e[type=item,tag=drill.rotator] at @s run function tutorial:rotate_drill



execute as @e[type=interaction,tag=block_detector] if data entity @s attack run function tutorial:rotate_drill

#execute as @e[type=interaction,tag=block_detector,nbt={attack:{}}] on attacker run execute as @s[nbt={"SelectedItem":{components: {"minecraft:item_name": {color: "blue", text: "DRILL ROTATOR", italic: 1b}, "minecraft:item_model": "minecraft:dropper", "minecraft:custom_data": {drill.rotator: 1b}}, id: "minecraft:item_frame"}}] run execute as @n[tag=tutorial.custom_block] at @s run function tutorial:bamboo_mosaic/break

#execute as @e[type=interaction,tag=block_detector,nbt={attack:{}}] on attacker run execute as @s[nbt={"SelectedItem":{components: {"minecraft:item_name": {color: "blue", text: "DRILL ROTATOR", italic: 1b}, "minecraft:item_model": "minecraft:dropper", "minecraft:custom_data": {drill.rotator: 1b}}, id: "minecraft:item_frame"}}] run execute as @n[tag=tutorial.custom_block] at @s run say hi

# function tutorial:bamboo_mosaic/break
execute as @e[type=interaction,tag=block_detector] if data entity @s attack run data remove entity @s attack



