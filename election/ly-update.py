import argparse, os, json, csv

parser = argparse.ArgumentParser()
parser.add_argument("year")
parser.add_argument("-c", "--commit", action = "store_const", const = True)
args = vars(parser.parse_args())

if args["commit"] == True:
    os.replace("old-codes-result.json", "old-codes.json")
    quit()

with open("old-codes.json", newline = "", encoding = "utf-8") as file:
    data = json.loads(file.read())

base = {}
with open("elbase.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        row = [s.lstrip("'") for s in row]
        if row[0] != "00" and row[4] == "0000":
            if row[3] == "000":
                base[row[0] + row[1]] = row[5].replace("台", "臺")
            elif row[3] != "000":
                base[row[0] + row[1] + row[3]] = row[5].replace("台", "臺")
            else:
                print(row)

for k in base:
    if len(k) > 5:
        base[k] = base[k[0:5]] + base[k]

d = {}
for k in base:
    if len(k) > 5:
        d[base[k]] = k

base = d
print(len(base))

for k in data["names"]:
    b = False
    for s in data["names"][k]:
        if s in base:
            if args["year"] not in data["ly-pr"]:
                data["ly-pr"][args["year"]] = {}
            data["ly-pr"][args["year"]][base[s]] = k
            del base[s]
            b = True
            break
        if b == True:
            break

print(base)

with open("old-codes-result.json", "w", newline = "", encoding = "utf-8") as file:
    file.write(json.dumps(data, indent = 2, ensure_ascii = False))
