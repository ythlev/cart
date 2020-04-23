import csv, json

year = "2008"

if int(year) < 2016:
    oc = {}
    with open("old_codes.json", newline = "", encoding = "utf-8") as file:
        codes = json.loads(file.read())[year]
        for k in codes:
            oc[k[0:5]] = codes[k][0:5]

cand = {}
with open("elcand-" + year + ".csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        row = [s.lstrip("'") for s in row]
        if row[2] != "00" and row[3] == "000":
            cand[row[0] + row[1] + row[2] + row[5]] = row[7]

el = {}
with open("elctks-" + year + ".csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        row = [s.lstrip("'") for s in row]
        if row[2] != "00" and row[3] == "000" and row[-1] == "*":
            el["_" + oc[row[0] + row[1]] + row[2]] = cand[row[0] + row[1] + row[2] + row[6]]

print(el)

colour = {
    "16": "#33a02c", #dpp
    "1": "#1f78b4", #kmt
    "999": "#666", #ind
    "90": "#ff7f00", #pfp
    "267": "#fbbe01", #npp
    "303": "#b15928", #tsp
    "106": "#c20f51", #npsu
}

with open("template (2007–2019).svg", newline = "", encoding = "utf-8") as file_in:
    with open(year + ".svg", "w", newline = "", encoding = "utf-8") as file_out:
        for row in file_in:
            if row.find("path id") > -1:
                for k, v in el.items():
                    if row.find(k) > -1:
                        file_out.write(row.replace('id="{}"'.format(k), 'fill="{}"'.format(colour[v])))
                        break
            else:
                file_out.write(row)
