import cart.cart
import csv

data = {}
with open("vill.csv", newline = "", encoding = "big5") as file:
    for row in csv.DictReader(file):
        try:
            data["_" + row["V_ID"].replace("-", "")] = float(row["P_DEN"])
        except:
            continue

cart.fill(
    template = "p-den",
    data = data
)
