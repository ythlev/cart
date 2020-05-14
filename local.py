import argparse, csv, cart

parser = argparse.ArgumentParser()
parser.add_argument("area")
parser.add_argument("winner index")
parser.add_argument("winner party")
parser.add_argument("runner-up index")
parser.add_argument("runner-up party")
args = vars(parser.parse_args())

code = {
    "New Taipei": "65000",
    "Taipei": "63000",
    "Taoyuan": "68000",
    "Taichung": "66000",
    "Tainan": "67000",
    "Kaohsiung": "64000",
    "Hsinchu": "10004",
    "Changhua": "10007",
    "Yunlin": "10009",
    "Pingtung": "10013"
}
vill = []
el, data = {}, {}

with open("election/local/elctks.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        row = [s.lstrip("'") for s in row]
        if (row[0] + row[1] == code[args["area"]] and
            row[3] != "000" and
            (args["area"] not in vill and row[4] == "0000") or
        (row[4] != "0000")):
            id = row[0] + row[1] + row[3]
            if args["area"] in vill:
                id = id + row[4][1:4]
            if row[6] not in [args["winner index"], args["runner-up index"]]:
                continue
            if id not in el:
                el[id] = {}
            el[id][row[6]] = int(row[7])
            if len(el[id]) == 2:
                data[id] = el[id][args["winner index"]] - el[id][args["runner-up index"]]

colours = {
    "dpp": ['#d9f0d3','#7fbf7b','#1b7837'],
    "kmt": ['#d1e5f0','#67a9cf','#2166ac'],
    "ind": ['#e0e0e0','#999999','#4d4d4d'],
    "mkt": ['#fff7bc','#fec44f','#d95f0e']
}

colours[args["runner-up party"]].reverse()
colour = colours[args["runner-up party"]] + colours[args["winner party"]]

cart.fill(
    template = "election/local/" + args["area"],
    data = data,
    colour = colour
)
