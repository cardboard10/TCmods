advancement revoke @s only tutorial:placed_item_frame
tag @s add tutorial.placed_item_frame
execute as @e[type=item_frame,tag=tutorial.item_frame_block,distance=..10] at @s run function tutorial:determine_block
tag @s remove tutorial.placed_item_frame