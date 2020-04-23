import cart, csv

data = {}
with open("population/vill.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.DictReader(file):
        try:
            data["_" + row["V_ID"].replace("-", "")] = float(row["P_DEN"])
        except:
            continue

cart.fill(
    template = "population/p-den",
    data = data,
    data_type = "seq"
)
