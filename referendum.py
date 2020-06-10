import json, csv, cart

data = {}

conv = {}
with open("election/old-codes.json", newline = "", encoding = "utf-8") as file:
    oc = json.loads(file.read())["names"]
    for code in oc:
        conv[oc[code][0]] = "_" + code

with open("election/referendum/data.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.DictReader(file):
        if row["行政區"] != "" and row["村里"] == "":
            data[conv[row["縣市"] + row["行政區"]]] = int(row["同意票數"]) - 0.25 * int(row["投票權人數"])

print(data)

cart.fill(
    template = "election/referendum/ref",
    data = data,
    area_keyword = "path id"
)
