scoreboard objectives add scale trigger scale
scoreboard players enable @a scale
scoreboard objectives add preset trigger preset
scoreboard players enable @a preset
execute as @a[scores={preset=0}] run function super-powers:clear
function super-powers:scale
function super-powers:breath
scoreboard objectives add oxygen_bonus trigger oxygen_bonus
scoreboard players enable @a oxygen_bonus
return run data get entity @p