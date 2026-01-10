data modify storage temp:macro block_id set from block ~ ~ ~ Items[{Slot:0b}].id

function your_namespace:macro_function with storage temp:macro

#item modify block ~ ~ ~ container.0 {"function": "minecraft:set_count", "count": -1, "add": true}
