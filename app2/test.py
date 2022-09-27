import ast

specieslist2 = []

with open("savedPeople.txt","r",encoding="utf8") as file:
    specieslist = file.readlines()
    for i in specieslist:
        specieslist2.append(ast.literal_eval(i))


for i in specieslist2:
    for j in i:
        print(j)
