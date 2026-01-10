execute if block ~ ~ ~ #minecraft:air run function tutorial:bamboo_mosaic/break
execute unless block ~ ~ ~ #minecraft:air if block ^ ^ ^1 #tutorial:mineable unless block ^ ^ ^1 #minecraft:incorrect_for_iron_tool if items block ~ ~ ~ container.0 minecraft:coal run function tutorial:bamboo_mosaic/mine
execute if items block ~ ~ ~ container.1 minecraft:coal if block ^ ^ ^1 #minecraft:air run function tutorial:bamboo_mosaic/move



execute unless block ~ ~ ~ #minecraft:air if block ^ ^ ^1 #tutorial:mineable unless block ^ ^ ^1 #minecraft:incorrect_for_iron_tool if items block ~ ~ ~ container.0 minecraft:charcoal run function tutorial:bamboo_mosaic/mine
execute if items block ~ ~ ~ container.1 minecraft:charcoal if block ^ ^ ^1 #minecraft:air run function tutorial:bamboo_mosaic/move

tp @n[type=interaction,tag=block_detector] ~ ~ ~ 0 0



execute as @n[type=minecraft:item_display] at @s run function tutorial:bamboo_mosaic/place_
