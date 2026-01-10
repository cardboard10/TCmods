# 1. Fill the area below with air, but 'loot' the items into the barrel first
# We loop through each Y level from -1 to -$(count) to collect drops
$loot insert ~ ~ ~ mine ~ ~-$(count) ~

# 2. Now fill the area with air (clearing the blocks)
$fill ~ ~-1 ~ ~ ~-$(count) ~ air

# 3. Remove exactly the coal stack from the first slot
item replace block ~ ~ ~ container.0 with air

