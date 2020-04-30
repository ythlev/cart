import argparse, csv, json

parser = argparse.ArgumentParser()
parser.add_argument("year")
args = vars(parser.parse_args())

if int(args["year"]) < 2016:
    oc = {}
    with open("election/old-codes.json", newline = "", encoding = "utf-8") as file:
        oc = json.loads(file.read())["ly-pr"][args["year"]]

party = {}
with open("election/ly-pr/elcand.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        row = [s.rstrip(" ").lstrip("'") for s in row]
        party[row[5]] = row[7]

el = {}
with open("election/ly-pr/elctks.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        row = [s.rstrip(" ").lstrip("'") for s in row]
        if row[3] != "000" and row[4] == "0000":
            id = row[6]
            if int(args["year"]) < 2016:
                id3 = "_" + oc[row[0] + row[1] + row[3]]
            else:
                id3 = "_" + row[0] + row[1] + row[3]
            if id3 not in el:
                el[id3] = {}
            if party[id] not in el[id3]:
                el[id3][party[id]] = 0
            el[id3][party[id]] += int(row[7])

data = {}
for town in el:
    leader, votes = "", 0
    for party in el[town]:
        if el[town][party] > votes:
            leader = party
            votes = el[town][party]
    data[town] = [leader, votes]

colour = {
    "1": ['#d1e5f0','#67a9cf','#2166ac'], #kmt
    "16": ['#d9f0d3','#7fbf7b','#1b7837'], #dpp
    "90": ['#fee6ce','#fdae6b','#e6550d'], #pfp
    "95": ['#f6e8c3','#d8b365','#8c510a'], #tsu
    "303": ['#f6e8c3','#d8b365','#8c510a'], #tsp
    "74": ['#fff7bc','#fec44f','#d95f0e'], #np
    "267": ['#fff7bc','#fec44f','#d95f0e'], #npp
    "106": ['#fde0dd','#fa9fb5','#c51b8a'], #npsu
    "999": ['#e0e0e0','#999999','#4d4d4d'], #ind
}

def fill(
    template, # name of template file name
    data, # dictionary of values where keys correspond to ids in the svg template
    data_type = "div", # "div"ering or "seq"uential data
    bands = 5, # for seq data; number of bands
    based = True, # for seq data; if data has a baseline value
    threshold = None, # list of threshold values
    colour = None, # list of colours to use
    area_keyword = 'Z" id', # keyword used to identify area paths
    replace_string = 'id="{}"' # string to replace, with format placeholder
):
    import statistics, math
    if threshold == None:
        values = []
        for area in data:
            values.append(abs(data[area][1]))
        mean = statistics.mean(values)
        if data_type == "seq":
            if colour == None:
                if bands == 5:
                    colour = ['#fef0d9','#fdcc8a','#fc8d59','#e34a33','#b30000']
                elif bands == 6:
                    colour = ['#fef0d9','#fdd49e','#fdbb84','#fc8d59','#e34a33','#b30000']
                elif bands == 7:
                    colour = ['#fef0d9','#fdd49e','#fdbb84','#fc8d59','#ef6548','#d7301f','#990000']
            if based == True:
                q = statistics.quantiles(values, n = 100, method = "inclusive")
            else:
                q = [0]
            mean_index = ((bands + 1) // 2)
            step = math.sqrt(mean - q[0]) / mean_index
            if threshold == None:
                threshold = []
                for i in range(bands):
                    threshold.append(math.pow(i * step, 2) + q[0])
        else:
            if colour == None:
                colour = ['#8c510a','#d8b365','#f6e8c3','#c7eae5','#5ab4ac','#01665e']
            if threshold == None:
                threshold = [0, -mean, -mean / 4, 0, mean / 4, mean]
    print("Thresholds:", ["{:.2f}".format(i) for i in threshold])
    with open(template + ".svg", newline = "", encoding = "utf-8") as file_in:
        with open(template + "-result.svg", "w", newline = "", encoding = "utf-8") as file_out:
            for row in file_in:
                if row.find(area_keyword) > -1:
                    for k, v in data.items():
                        if row.find(k) > -1:
                            i = 0
                            while i < bands - 1:
                                if v[1] >= threshold[i + 1]:
                                    i += 1
                                else:
                                    break
                            file_out.write(row.replace(replace_string.format(k), 'fill="{}"'.format(colour[v[0]][i])))
                            break
                else:
                    file_out.write(row)

fill(
    template = "election/ly-pr/pr",
    data = data,
    data_type = "seq",
    colour = colour,
    based = False,
    area_keyword = "path id",
    bands = 3
)
