import csv

def export_csv(positions):

    with open("resonators.csv","w") as f:

        writer = csv.writer(f)

        for p in positions:

            writer.writerow(p)