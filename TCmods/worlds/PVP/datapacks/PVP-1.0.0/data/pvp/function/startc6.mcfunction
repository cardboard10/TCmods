function pvp:clear
trigger class set 6
give @s minecraft:trident[minecraft:enchantments={quick_charge:5,riptide:5,piercing:5,loyalty:5,fire_aspect:255,channeling:255,respiration:255}]
give @s minecraft:trident[minecraft:enchantments={quick_charge:5,loyalty:5,channeling:255,fire_aspect:255,riptide:1}]
give @s minecraft:turtle_helmet
give @s minecraft:chainmail_chestplate
give @s minecraft:chainmail_leggings
give @s minecraft:chainmail_boots
attribute @s minecraft:oxygen_bonus base set 999999999999
attribute @s minecraft:submerged_mining_speed base set 2
attribute @s minecraft:water_movement_efficiency base set 100
dialog show @s pvp:tp