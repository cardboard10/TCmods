execute at @s anchored feet align xyz run tp @s ~0.5 ~0 ~0.5



setblock ~ ~ ~ barrel keep
#execute if block ~ ~ ~ water run setblock ~ ~ ~ glass
execute align y run summon item_display ~ ~ ~ {Tags:["tutorial.custom_block","tutorial.bamboo_mosaic"],transformation:{left_rotation:[0f,0f,0f,0.1f],right_rotation:[0f,0f,0f,0.1f],translation:[-0f,0.5f,-0f],pivot:[5.0f,5.0f,5.0f],scale:[1.03f,1.03f,1.03f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:item_model":"minecraft:dispenser"}}}
#,brightness:{sky:15,block:15}

summon minecraft:interaction ~ ~ ~ {Tags:["block_detector"],width:0.8f,height:1.2f,response:1b}

execute as @e[type=minecraft:item_display] at @s run function tutorial:bamboo_mosaic/place_

execute as @e[type=minecraft:item_display] at @s run function tutorial:bamboo_mosaic/macro_function
