num = 100
data = {}
for x in range (884,902,17):
    for y in range (0, 69, 17):
        num +=1
        data[f"weapon_{num}"] = {"pos":(x,y), "category":"weapon", "stats":{"attack":3, "speed":-1}}
for k,v in data.items():
 print(f'"{k}":{v},')
print(num)