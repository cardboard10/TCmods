#kill @e[type=!minecraft:player,type=!snowball,type=!wind_charge,type=!slime,type=!lightning_bolt,type=!arrow,type=!trident]
#execute at @e[type=snowball] run fill ~-3 ~-3 ~-3 ~3 ~3 ~3 air replace minecraft:lava
#execute at @e[type=snowball] run setblock ^ ^ ^1 lava
#execute at @a run fill ~-10 ~-10 ~-10 ~10 ~10 ~10 air replace minecraft:lava
#execute at @a run fill ~-10 ~-3 ~-10 ~10 ~10 ~10 air replace minecraft:lava
#execute at @a run fill ~-10 ~-2 ~-10 ~10 ~10 ~10 air replace minecraft:lava
#execute at @a run fill ~-10 ~-1 ~-10 ~10 ~10 ~10 air replace minecraft:lava
#execute at @a run fill ~-10 ~ ~-10 ~10 ~10 ~10 air replace minecraft:lava
#give @a dirt[minecraft:equippable={slot:head},minecraft:custom_name=try_this_helmet_on,minecraft:attribute_modifiers=[{"amount":1,"id":"ld","operation":"add_multiplied_total",type:"scale","slot":"head"}],minecraft:max_stack_size=99] 99
execute as @a[scores={class=0}] run function pvp:clear
execute as @a[scores={class=0}] run effect clear @s


#execute at @e[nbt={Item:{components:{"minecraft:custom_name":"VilHouse1"}}}] as @e[nbt={Item:{components:{"minecraft:custom_name":"VilHouse1"}}}] run function pvp:vilhouse1
#execute at @e[nbt={Item:{components:{"minecraft:custom_name":"VilHouse1"}}}] as @e[nbt={Item:{components:{"minecraft:custom_name":"VilHouse1"}}}] run fill ~-1 ~-1 ~-1 ~1 ~1 ~1 water

#scoreboard players set @e[nbt={Item:{components:{"minecraft:custom_name":"VilHouse1"}}}] type 1

#execute as @e[scores={type=1}] at @e[scores={type=1}] run execute unless block ~ ~-.4 ~ #minecraft:air run execute as @e[limit=30] run summon minecraft:tnt ~ ~ ~ {Motion:[0,1,0]}
#	place template pvp:house1 ~ ~ ~



execute as @a[scores={class=1}] run function pvp:tickc1

execute as @a[scores={class=2}] run function pvp:tickc2

execute as @a[scores={class=3}] run function pvp:tickc3

execute as @a[scores={class=4}] run function pvp:tickc4

execute as @a[scores={class=5}] run function pvp:tickc5

execute as @a[scores={class=6}] run function pvp:tickc6

scoreboard players display numberformat @a class styled {}


function pvp:test

execute as @a[scores={tp=1}] run tp @n[name=arena]

execute as @a[scores={tp=2}] run tp @n[name=log_out]

execute as @a[scores={tp=3}] run tp @n[name=sea]

scoreboard players set @a[scores={tp=1..3}] tp 0

execute as @a[scores={start=1}] run function pvp:start

scoreboard players set @a start 0

execute as @a[scores={tp=1}] run say tp1


execute as @a[scores={deaths=1}] run scoreboard players set @s tclass 0
execute as @a[scores={deaths=1}] run scoreboard players set @s class 0
execute as @a[scores={deaths=1}] run scoreboard players set @s ttp 0
execute as @a[scores={deaths=1}] run scoreboard players set @s tp 0
execute as @a[scores={deaths=1}] run dialog show @s pvp:class
execute as @a[scores={deaths=1}] run say pick your class
execute as @a[scores={deaths=1}] run scoreboard players enable @a tclass
execute as @a[scores={deaths=1}] run scoreboard players enable @a ttp
execute as @a[scores={deaths=1}] run scoreboard players set @s deaths 2



execute as @a[scores={deaths=2,tclass=1}] run scoreboard players set @s class 1
execute as @a[scores={deaths=2,tclass=2}] run scoreboard players set @s class 2
execute as @a[scores={deaths=2,tclass=3}] run scoreboard players set @s class 3
execute as @a[scores={deaths=2,tclass=4}] run scoreboard players set @s class 4
execute as @a[scores={deaths=2,tclass=5}] run scoreboard players set @s class 5
execute as @a[scores={deaths=2,tclass=6}] run scoreboard players set @s class 6
execute as @a[scores={deaths=2,tclass=1..6}] run scoreboard players set @s deaths 3

execute as @a[scores={deaths=3,ttp=0}] run function pvp:start
execute as @a[scores={deaths=3,ttp=0}] run dialog show @s pvp:tp
execute as @a[scores={deaths=3,ttp=0}] run scoreboard players set @s deaths 4

execute as @a[scores={deaths=4,ttp=1}] run scoreboard players set @s tp 1
#execute as @a[scores={deaths=4,ttp=1}] run say ttp1
execute as @a[scores={deaths=4,ttp=2}] run scoreboard players set @s tp 2
execute as @a[scores={deaths=4,ttp=3}] run scoreboard players set @s tp 3
execute as @a[scores={deaths=4,ttp=1..3}] run scoreboard players set @s deaths 0


#execute at @e[type=minecraft:snowball] run fill ~-3 ~-3 ~-3 ~3 ~3 ~3 air replace
#tp jumping_llama key_Kiy
#execute at @e[name=cave] run fill ~-5 ~-5 ~-5 ~5 ~5 ~5 dirt
#execute at key_Kiy run function mega_fill
#dialog clear @a

