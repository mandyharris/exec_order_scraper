#This program is written in Python 2.7 to gather the dates of the signing
#of each presidential executive order from 1937 through 2016, and determine
#how many days past inauguration that each was signed.

#the goal is to gather data to determine the rate at which presidents sign
#executive orders.

from bs4 import BeautifulSoup
import urllib2
import csv
import datetime
import datefinder

#the extractor function is the part that actually does the scraping and the output

#it takes the year to put in the url, the file to write to
#the date of inauguration
#and the count (number of orders signed so far) for the current president

#it runs once for each year (or twice in years with two presidents)

count = 0

def extractor( year, f, i_date, prev_order_num ):
	print 'Scraping', year

	global count

	#fairly self explanatory. url_start holds the beginning that is in every
	#link, and url combines it with the year (or year-president) and ".html"
	url_start = "http://www.archives.gov/federal-register/executive-orders/"
	url = url_start + year + ".html"

	#opens the page, let BeautifulSoup do its magic to make it scrapable
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "lxml")

	#gets the specific div from the page containing the data I want
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

			#eisenhower '56 typo: October 22, 19656. How do I fix that?

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


year = 1937	#starting year
count = 1715	#starting count (starts partway through FDR's presidency)

#first file to write to
file = csv.writer(open("1937-roosevelt_orders.csv", "w"))
file.writerow(["Order Number", "Day Number"])
file.writerow([0, 0])

#the archive.gov site has most url's with just the year, but in years when
#the presidency changes hands, it adds the president's last name

#skip_list is a list of the years when the presidency changed hands
#skipped_list is a list of what will go in place of the year in the url

skip_list = []
skipped_list = []
inaug_list = []

with open("years_names.csv", "rb") as filein:
	reader = csv.reader(filein)
	input = list(reader)

for x in range(len(input)-1):
	skip_list.append(input[x][0])
	skipped_list.append(input[x][0] + "-" + input[x][1])
	skipped_list.append(input[x][0] + "-" + input[x+1][1])


for item in input:
	inaug_list.append(item[2])

#to hold list of inaugural dates
inaugurations = []

for item in inaug_list:
	matches = datefinder.find_dates(item)
	for match in matches:
		inaugurations.append(match.date())

skip_index = 0	#starting index for skipped list
i_index = 0	#starting index for inaugurations list

#initialize variable used to check for repeats
prev_order_num = " "

#loop through years from 1937 through 2016
while (year < 2017):
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
		file = csv.writer(open(skipped_list[skip_index] + "_orders.csv", "w"))
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

