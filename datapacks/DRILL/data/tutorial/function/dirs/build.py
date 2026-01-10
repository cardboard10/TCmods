import os

def PLACE(block):
    return f"""execute at @s anchored feet align xyz run tp @s ~0.5 ~ ~0.5



setblock ~ ~ ~ scaffolding keep
#execute if block ~ ~ ~ water run setblock ~ ~ ~ scaffolding
execute align y run summon item_display ~ ~ ~ {{Tags:["tutorial.custom_block","tutorial.{block}"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.5f,0f],scale:[1.01f,1.01f,1.01f]}},item:{{id:"minecraft:item_frame",count:1,components:{{"minecraft:item_model":"minecraft:{block}"}}}}}}
#,brightness:{{sky:15,block:15}}"""

def TICK(block):
    return f"""execute if block ~ ~ ~ #minecraft:air run function tutorial:{block}/break"""

def BREAK(block):
    return f"""
kill @s
kill @n[type=item,nbt={{OnGround:0b,Age:0s}}]
loot spawn ~ ~0.5 ~ loot tutorial:{block}"""


def make(dir,block):
    os.mkdir(block)
    with open(f"{block}/break.mcfunction","x") as file:
        file.writelines(BREAK(block))
    with open(f"{block}/tick.mcfunction","x") as file:
        file.writelines(TICK(block))
    with open(f"{block}/place.mcfunction","x") as file:
        file.writelines(PLACE(block))

blocks=[
    "deepslate_tiles",
    "deepslate_bricks",
    "bamboo_block",
    "bamboo_mosaic",
    "deepslate_tile_slab",
    "deepslate_brick_slab",
    "bamboo_slab",
    "bamboo_mosaic_slab",
    "deepslate_tile_stairs",
    "deepslate_brick_stairs",
    "bamboo_stairs",
    "bamboo_mosaic_stairs"
]

for block in blocks:
    make("C:/Users/maste/OneDrive/Desktop/LD/py/MCserver/world/datapacks/WASD Custom Block Tutorial Datapack 1.21.4/data/tutorial/function/dirs",block)
