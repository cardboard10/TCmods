clear @s
function pvp:clear
trigger class set 1
effect give @s minecraft:regeneration 35
attribute @s minecraft:movement_speed base set .075
attribute @s minecraft:max_health base set 40
attribute @s minecraft:armor base set 5
attribute @s minecraft:scale base set 1.5
dialog show @s pvp:tp
give @s shield
give @s stone_sword
give @s minecraft:wooden_sword[minecraft:break_sound=entity.enderman.scream,minecraft:max_damage=10,minecraft:damage=9]


