clear @s
function pvp:clear
effect clear @s
trigger class set 2
attribute @s minecraft:movement_speed base set .15
attribute @s minecraft:fall_damage_multiplier base set 0.5
attribute @s minecraft:safe_fall_distance base set 5
attribute @s minecraft:max_health base set 12
attribute @s minecraft:jump_strength base set .72

give @s minecraft:chainmail_helmet[minecraft:unbreakable={}]
give @s minecraft:chainmail_chestplate[minecraft:unbreakable={}]
give @s minecraft:chainmail_leggings[minecraft:unbreakable={}]
give @s minecraft:chainmail_boots[minecraft:unbreakable={}]

give @s arrow
give @s bow[minecraft:enchantments={power:6,punch:6,infinity:1,multishot:2,unbreaking:255}]
schedule function pvp:invisible 10s
dialog show @s pvp:tp