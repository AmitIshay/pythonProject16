import csv
import re
import json

data = {"csvToJsonFile": []}


with open("new_table.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) >= 11:
            data["csvToJsonFile"].append({
                "ID": row[0],
                "fullName": row[1],
                "prefix": row[2],
                "statePrefix": row[3],
                "mobileNumber": row[4],
                "state": row[5],
                "city": row[6],
                "neighborhood": row[7],
                "street": row[8],
                "houseDetails1": row[9],
                "houseDetails2": row[10]
            })
        else:
            print(f"Row skipped: {row}")

with open("csvToJsonFile.json", "w") as f:
    json.dump(data, f, indent=4)