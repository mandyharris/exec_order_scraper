#This program is written in Python 2.7 to show the rates at which each president
#has signed executive orders over the course of their presidency. The data is
#mostly gathered from scraping the Executive Orders Disposition Tables on the
#Federal Register Archives website. The second section is to get the data that
#isn't in the Disposition Tables, but in a CSV, and to format that data to match
#the scraped data. The third and final section takes all the data generated by
#the first two sections and displays it on a graph.

from bs4 import BeautifulSoup
import urllib
import urllib2
import csv
import datetime
import datefinder
import matplotlib.pyplot as plt
import numpy

#SECTION 1: Scraping from the website

#the extractor function is the part that actually does the scraping and the
#output it takes the year to put in the url, the file to write to the date of
#inauguration and the count (number of orders signed so far) for the current
#president
#it runs once for each year (or twice in years with two presidents)

def extractor( year, f, i_date, prev_order_num ):
    print 'Scraping', year

    global count

    #fairly self explanatory. url_start holds the beginning that is in every
    #link, and url combines it with the year (or year-president) and ".html"
    url_start = "http://www.archives.gov/federal-register/executive-orders/"
    url = url_start + year + ".html"

    #opens the page, let BeautifulSoup do its magic to make it scrapeable
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "lxml")

    #gets the specific div from the page containing the desired data
    div = soup.find("div", {"class" : "region region-content"})
    date_list = div.findAll("ul")
    order_num_list = div.findAll("p")


    new_order_num_list = []

    #remove sets of empty p tags in order_num_list
    for item in order_num_list:
        if (str(item) != "<p></p>"):
            new_order_num_list.append(item)


    #each date is in a separate "ul", the first "li" of each
    for x in range(len(date_list)):

        #get list item with day order was signed
        items = date_list[x].findAll("li")
        date_signed_original = items[0].find(text=True)

        #get official order number
        order_num_str = new_order_num_list[x].findAll(text=True)
        order_num = order_num_str[-1].strip()

        #make sure orders aren't counted twice
        if (order_num != prev_order_num):


            #correcting typos from the website for accurate data
            date_signed = date_signed_original.replace(".", ",")
            date_signed = date_signed.split(",")[0] + " " + year

            #extract the date from the text
            matches = datefinder.find_dates(date_signed)

            #datefinder puts the dates in a list, so even though there's only
            #one date, this is necessary
            for match in matches:
                #to determine the days since inauguration on which
                #the order was signed
                day_num = abs((match.date() - i_date).days)

                #write order count and number of days to csv
                f.writerow([count, day_num])

                #increment order count
                count = count + 1

            prev_order_num = order_num

    return prev_order_num

#to convert string with date to python datetime format
def get_date(date):
    matches = datefinder.find_dates(date)
    for match in matches:
        py_date = match.date()
        return py_date


year = 1937    #starting year
count = 1715 #starting count (starts partway through FDR's presidency)

#first file to write to
file = csv.writer(open("1937-roosevelt_orders.csv", "w"))
file.writerow(["Order Number", "Day Number"])
file.writerow([0, 0])

#the archive.gov site has most url's with just the year, but in years when
#the presidency changes hands, it adds the president's last name

#file_list is a list of the CSVs created by this program in the first and second
#sections for the third section to reference
file_list = ["1937-roosevelt_orders.csv"]

#skip_list is a list of the years when the presidency changed hands
#skipped_list is a list of what will go in place of the year in the url

skip_list = []
skipped_list = []
inaug_list = []

with open("metadata.csv", "rb") as filein:
    reader = csv.reader(filein)
    input = list(reader)


for x in range(len(input)):
    skip_list.append(input[x][0])
    skipped_list.append(input[x][0] + "-" + input[x][1])
    if (input[x][0] != "2017"):
        skipped_list.append(input[x][0] + "-" + input[x+1][1])


for item in input:
    inaug_list.append(item[2])

#to hold list of inaugural dates
inaugurations = []

for item in inaug_list:
    inaugurations.append(get_date(item))

skip_index = 0    #starting index for skipped list
i_index = 0    #starting index for inaugurations list

#initialize variable used to check for repeats
prev_order_num = " "

#loop through years from 1937 through 2016
while (year < 2018):
    #initalize bool to check for years to skip
    skip_year = False
    #check if year should be skipped
    for skip in skip_list:
        if (str(year) == skip):
            skip_year = True

    #non-skip year
    if (skip_year == False):
        #pass year, file, inaugural date, and exec order count
        prev_order_num = extractor(str(year), file, inaugurations[i_index], prev_order_num)

    #skip year
    else:
        #pass "year-president" string, file, inaugural date
        #and exec order count
        prev_order_num = extractor(skipped_list[skip_index], file, inaugurations[i_index], prev_order_num)
        #increment index for skipped list
        skip_index = skip_index + 1

        #switch presidents

        #open new file with "year-president" string in filename
        if (year < 2017):
            new_file_name = skipped_list[skip_index] + "_orders.csv"
            file = csv.writer(open(new_file_name, "w"))
            file_list.append(new_file_name)
            file.writerow(["Order Number", "Day Number"])
            file.writerow([0, 0])
            #increment index for new inaugural date
            i_index = i_index + 1
            #reset exec order count
            count = 1

            #I could've made this a separate function or something as this
            #code is repeated but it seemed like a waste for only two lines
            prev_order_num = extractor(skipped_list[skip_index], file, inaugurations[i_index], prev_order_num)
            skip_index = skip_index + 1

    #increment year
    year = year + 1

#SECTION 2: Getting data from the CSV for Trump

#because they changed formatting and are now using CSVs
#but only as far back as 1994
#so this will only be used for Trump for now
#if they add back to 1937 in this format, section 1 will be erased and
#replaced by this section

url = "https://www.federalregister.gov/documents/search.csv?conditions%5Bcorrection%5D=0&conditions%5Bpresident%5D=donald-trump&conditions%5Bpresidential_document_type_id%5D=2&conditions%5Btype%5D=PRESDOCU&fields%5B%5D=citation&fields%5B%5D=document_number&fields%5B%5D=end_page&fields%5B%5D=executive_order_notes&fields%5B%5D=executive_order_number&fields%5B%5D=html_url&fields%5B%5D=pdf_url&fields%5B%5D=publication_date&fields%5B%5D=signing_date&fields%5B%5D=start_page&fields%5B%5D=title&order=executive_order_number&per_page=1000"

urllib.urlretrieve(url, "trump.csv")

#open read file
with open("trump.csv", "rb") as filein:
    reader = csv.reader(filein)
    input = list(reader)

#and write file
f = open("2017-trump_orders.csv", "w")
file = csv.writer(f)
file_list.append("2017-trump_orders.csv")
file.writerow(["Order Number", "Day Number"])
file.writerow([0, 0])

#orders can be counted simply by incrementing with each row
count = 1

#we want to count the days since inauguration, not just list dates
#so we need to put in the date of inauguration and subtract that from each
#signing date
i_date = get_date("January 20, 2017")

print("Scraping Trump")

for x in range(len(input)-1):
    order_num = count
    sign_date = get_date(input[x+1][8])
    day_count = abs((sign_date - i_date).days)
    file.writerow([order_num, day_count])
    count = count + 1

f.close()
#SECTION 3: Plotting the data

#starting lists
name_list = ["roosevelt"]
party_list = ["democrat"]

#get ~metadata
with open("metadata.csv", "rb") as filein:
    reader = csv.reader(filein)
    input = list(reader)

#put metadata in lists
for x in range(len(input)-1):
    name_list.append(input[x+1][1])
    party_list.append(input[x+1][3])

#ending lists, entries aren't in metadata.csv for some wacky reason
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

#make the plot lines
for i in range(len(party_list)):
    dash = "--"

    #import CSV
    with open(file_list[i], "rb") as readfile:
        reader = csv.reader(readfile)
        data = list(reader)

    x_vals = []
    y_vals = []
    #read info to lists
    for j in range(len(data)-1):
        x_vals.append(int(data[j+1][0]))
        y_vals.append(int(data[j+1][1]))

    if(party_list[i] == "democrat"):
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

    plt.plot(y_vals, x_vals, color = line_color, ls = dash, label = name_list[i])

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
