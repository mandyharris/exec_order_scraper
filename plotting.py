import matplotlib.pyplot as plt
import numpy
import csv

#starting lists
file_list = ["1937-roosevelt_orders.csv"]
name_list = ["roosevelt"]
party_list = ["democrat"]

#get ~metadata
with open("years_names.csv", "rb") as filein:
	reader = csv.reader(filein)
	input = list(reader)

#put metadata in lists
for x in range(len(input)-1):
    to_append = (input[x][0] + "-" + input[x+1][1] + "_orders.csv")
    file_list.append(to_append)
    name_list.append(input[x+1][1])
    party_list.append(input[x+1][3])

#ending lists, entries aren't in years_names.csv for some wacky reason
file_list.append("2017-trump_orders.csv")
name_list.append("trump")
party_list.append("republican")

#lists of colors for each political party
reds = ["#ffaeae", "#fd5757", "#d21919", "#000000"]
blues = ["#acd3f9", "#4c99e5", "#0064c9", "#004283"]

#variables to keep the line colors/styles in order
redcount = 0
bluecount = 0
reddash = False
bluedash = False
dash = "--"

t = numpy.arange(0., 5., 0.2)

#make the plot lines
for x in range(len(party_list)):
    #import CSV

    with open(file_list[x], "rb") as readfile:
        reader2 = csv.reader(readfile)
        data = list(reader2)

    x_vals = []
    y_vals = []
    #read info to lists
    for i in range(len(data)-1):
        x_vals.append(int(data[i+1][0]))
        y_vals.append(int(data[i+1][1]))

    if(party_list[x] == "democrat"):
        line_color = blues[bluecount]
        if(bluedash):
            dash = "-."
            bluecount = bluecount + 1
        bluedash = not bluedash
    else:
        line_color = reds[redcount]
        if(reddash):
            dash = "-."
            redcount = redcount + 1
        reddash = not reddash

    plt.plot(y_vals, x_vals, color = line_color, ls = dash, label = name_list[x])
    dash = "--"

#import data from CSVs
#plot data

#future: combine scripts, pandas dataframes?

plt.legend(loc = "upper left")

#to focus on trump
plt.axis([0, 450, 0, 80])

#to focus on eisenhower (good display of all except truman and roosevelt)
#plt.axis([0, 3000, 0, 500])

#to focus on roosevelt (because he skews the scales so much)
#plt.axis([0, 4500, 0, 3800])


plt.ylabel("Orders Signed")
plt.xlabel("Days in Office")
plt.show()
