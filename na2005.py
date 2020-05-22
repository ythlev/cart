import argparse, json, csv, cart

parser = argparse.ArgumentParser()
parser.add_argument("area")
parser.add_argument("-y", "--year")
args = vars(parser.parse_args())

code = {
    "New Taipei": "65000",
    "Taipei": "63000",
    "Taoyuan": "68000",
    "Taichung": "66000",
    "Tainan": "67000",
    "Kaohsiung": "64000",
    "Yilan": "10002",
    "Hsinchu": "10004",
    "Miaoli": "10005",
    "Changhua": "10007",
    "Nantou": "10008",
    "Yunlin": "10009",
    "Chiayi": "10010",
    "Pingtung": "10013",
    "Taitung": "10014",
    "Hualien": "10015"
}
el, data = {}, {}

if args["year"] != None:
    with open("election/old-codes.json", newline = "", encoding = "utf-8") as file:
        oc = json.loads(file.read())["NA"][args["year"]]

p = {
    "y": ["3", "7", "8", "9", "10"],
    "n": ["1", "2", "4", "5", "6", "11", "12"]
}

with open("election/NA/elctks.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        row = [s.lstrip("'") for s in row]
        if row[3] == "000" or row[4] != "0000":
            continue
        id = row[0] + row[1] + row[3]
        if id not in el:
            el[id] = {"i": 0}
        for t in p:
            if t not in el[id]:
                el[id][t] = 0
            if row[6] in p[t]:
                el[id][t] += int(row[7])
                el[id]["i"] += 1
        if el[id]["i"] == 12:
            if "oc" in globals():
                data["_" + oc[id]] = el[id]["y"] - el[id]["n"]
            else:
                data[id] = el[id]["y"] - el[id]["n"]

cart.fill(
    template = "election/NA/" + args["area"],
    data = data,
    area_keyword = "path id"
)
