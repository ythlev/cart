import csv, cart

conv = {}
with open("election/kh2020/town-2.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        conv[row[1]] = row[0]

area = {}
with open("election/kh2020/data.csv", newline = "", encoding = "utf-8") as file:
    for row in csv.reader(file):
        area[conv[row[0]]] = {
        "value": int(row[1]) - round(0.25 * int(row[2])),
        "weight": int(row[2])
    }

cart.fill(
    template = "election/kh2020/Kaohsiung",
    data = area
)
