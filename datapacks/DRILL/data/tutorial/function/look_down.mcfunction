rotate @s facing ~ ~-1 ~

data modify entity @s transformation.translation set value [0f,0f,-0.5f]

tp @n[type=interaction,tag=block_detector] @s
