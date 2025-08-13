import pathlib

def w(file,s=""):
    o=open(file,"w")
    o.writelines([s])
    o.close()
def r(file):
    o=open(file,"r")
    r=o.readlines()
    o.close()
    return r
def x(file,s=""):
    o=open(file,"x")
    o.writelines([s])
    o.close()
def X(file):
    pathlib.Path.mkdir(file)
name=input("name")
pack="""{
  "pack": {
    "description": "NAME",
    "pack_format": 81
  }
}
"""
pack=pack.replace("NAME",name)
recipe="""
{
  "type": "minecraft:crafting_shaped",
  "category": "redstone",
  "group": "wooden_door",
  "key": {
    "a": "minecraft:a:",
    "b": "minecraft:b:",
    "c": "minecraft:c:",
    "d": "minecraft:d:",
    "e": "minecraft:e:",
    "f": "minecraft:f:",
    "g": "minecraft:g:",
    "h": "minecraft:h:",
    "i": "minecraft:i:"
  },
  "pattern": [
    "abc",
    "def",
    "ghi"
  ],
  "result": {
    "count": 1,
    "id": "minecraft:out"
  }
}
"""

X(name)
x((name+"/"+"pack.mcmeta"),pack)
X(name+"/"+"data")
X(name+"/"+"data"+"/"+name)

rname=input("recipe name")
print("""
a|b|c
-----   ___
d|e|f  |out|
-----   ---
g|h|i
""")
X(name+"/"+"data"+"/"+name+"/"+"recipe")
L=["","","","","","","","","",""]
L[0]=input("a")
L[1]=input("b")
L[2]=input("c")
L[3]=input("d")
L[4]=input("e")
L[5]=input("f")
L[6]=input("g")
L[7]=input("h")
L[8]=input("i")
L[9]=input("out")
for I in range(len(L)):
    if L[I]=="":
        L[I]="air"
a=L[0]
b=L[1]
c=L[2]
d=L[3]
e=L[4]
f=L[5]
g=L[6]
h=L[7]
i=L[8]
out=L[9]

x((name+"/"+"data"+"/"+name+"/"+"recipe/"+rname+".json"),recipe.replace("a:",a).replace("b:",b).replace("c:",c).replace("d:",d).replace("e:",e).replace("f:",f).replace("g:",g).replace("h:",h).replace("i:",i).replace("out",out))
#x((name+"/"+"data"+"/"+name+"/"+"recipe/"+rname+".json"),recipe.replace("a:",input("a")).replace("b:",input("b")).replace("c:",input("c")).replace("d:",input("d")).replace("e:",input("e")).replace("f:",input("f")).replace("g:",input("g")).replace("h:",input("h")).replace("i:",input("i")).replace("o:",input("out")))
