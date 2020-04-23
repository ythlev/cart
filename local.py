import argparse, csv, cart

parser = argparse.ArgumentParser()
parser.add_argument("area")
parser.add_argument("winner index")
parser.add_argument("winner party")
parser.add_argument("runner-up index")
parser.add_argument("runner-up party")
args = vars(parser.parse_args())

code = {
    "Taipei": "63",
    "Kaohsiung": "64",
    "Tainan": "67"
}
vill = ["Taipei"]
el, data = {}, {}

with open("election/local/elctks.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        row = [s.lstrip("'") for s in row]
        if (row[0] == code[args["area"]] and
            row[3] != "000" and
            (args["area"] in ["Kaohsiung", "Tainan"] and row[4] == "0000") or
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
    "dpp": ['#41ab5d','#238b45','#005a32'],
    "kmt": ['#4292c6','#2171b5','#084594'],
    "ind": ['#737373','#525252','#252525']
}

colours[args["runner-up party"]].reverse()
colour = colours[args["runner-up party"]] + colours[args["winner party"]]

cart.fill(
    template = "election/local/" + args["area"],
    data = data,
    colour = colour
)
