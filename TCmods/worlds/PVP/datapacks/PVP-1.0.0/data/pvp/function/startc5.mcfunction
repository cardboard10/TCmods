function pvp:clear
clear @s
effect clear @s
trigger class set 5
give @s mace
give @s wind_charge 32


effect give @s minecraft:fire_resistance infinite

give @s minecraft:golden_helmet[minecraft:unbreakable={}]
give @s minecraft:golden_chestplate[minecraft:unbreakable={}]
give @s minecraft:golden_leggings[minecraft:unbreakable={}]
give @s minecraft:golden_boots[minecraft:unbreakable={}]
give @s minecraft:wooden_sword[minecraft:break_sound=entity.enderman.scream,minecraft:max_damage=10,minecraft:damage=9]

scoreboard players set @s usemace 0

dialog show @s pvp:tp