import csv, cart

el = {}
main = {}
with open("elctks-2018.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        row = [s.lstrip("'") for s in row]
        if row[0] == "64" and row[3] != "000" and row[4] == "0000":
            id = "_" + row[0] + row[1] + row[3]
            if row[6] != "1" and row[6] != "2":
                continue
            if id not in el:
                el[id] = {}
            el[id][row[6]] = int(row[7])
            if len(el[id]) == 2:
                main[id] = el[id]["1"] - el[id]["2"]

colours = {
    "dpp": ['#41ab5d','#238b45','#005a32'],
    "kmt": ['#4292c6','#2171b5','#084594'],
    "ind": ['#737373','#525252','#252525']
}

w, ru = "kmt", "dpp"

colours[ru].reverse()
colour = colours[ru] + colours[w]

cart.fill(
    template = "2018 Kaohsiung",
    data = main,
    colour = colour
)
