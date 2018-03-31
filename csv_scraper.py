#because they changed formatting and are now using CSVs
#but only as far back as 1994
#so I'm only going to use this for Trump for now
#if they add back to 1937 in this format, I'll update and use it for all
import csv
import datetime
import datefinder

def get_date(date):
    matches = datefinder.find_dates(date)
    for match in matches:
        py_date = match
        return py_date

#open read file
with open("trump.csv", "rb") as filein:
    reader = csv.reader(filein)
    input = list(reader)

#and write file
file = csv.writer(open("2017-trump_orders.csv", "w"))
file.writerow(["Order Number", "Day Number"])
file.writerow([0, 0])

#instead of counting orders at 13765, we want to start at 1, so we need to
#adjust the numbers
adjustment = int(input[1][4]) - 1

#we also want to count the days since inauguration, not just list dates
#so we need to put in the date of inauguration and subtract that from each
#signing date
i_date = get_date("January 20, 2017")

for x in range(len(input)-1):
    order_num = int(input[x+1][4]) - adjustment
    sign_date = get_date(input[x+1][8])
    day_count = abs((sign_date - i_date).days)
    file.writerow([order_num, day_count])
