function pvp:clear
clear @s

effect clear @s
trigger class set 4
give @s minecraft:netherite_axe
give @s minecraft:golden_helmet
give @s minecraft:leather_chestplate
give @s minecraft:leather_leggings
give @s minecraft:leather_boots
attribute @s minecraft:movement_speed base set .13
attribute @s minecraft:entity_interaction_range base set 3.5
attribute @s minecraft:jump_strength base set .55


dialog show @s pvp:tp