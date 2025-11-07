num = 0
data = {}
for x in range (102,290,17):
    for y in range (0, 154, 17):
        num +=1
        data[f"shirt_{num}"] = {"pos": (x, y), "category": "shirt", "stats": {"defense": 1, "speed": 0}}
for k,v in data.items():
 print(f'"{k}":{v},')
print(num)