#This program is written to gather the dates of the signing of each presidential
#executive order from 1937 through 2016, and determine how many days past
#inauguration that each was signed.

#the goal is to gather data to determine the "normal rate" at which presidents
#sign executive orders.

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

def extractor( year, f, i_date, count ):
	print 'Scraping', year

	#fairly self explanatory. url_start holds the beginning that is in every
	#link, and url combines it with the year (or year-president) and ".html"
	url_start = "http://www.archives.gov/federal-register/executive-orders/"
	url = url_start + year + ".html"

	#opens the page, let BeautifulSoup do its magic to make it scrapable
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "lxml")

	#gets the specific div from the page containing the data I want
	div = soup.find("div", {"class" : "region region-content"})

	#each date is in a separate "ul", the first "li" of each
	for list in div.findAll("ul"):
		items = list.findAll("li")
		date_signed = items[0].find(text=True)

		#there were a few instances of a "." in the date instead of a
		#"," which caused datefinder to read them as separate dates
		#so this was added to remove them
		date_signed = date_signed.replace(".", "")

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



year = 1937	#starting year
count = 1715	#starting count (starts partway through FDR's presidency)

#first file to write to
file = csv.writer(open("1937-roosevelt_orders.csv", "w"))

#the archive.gov site has most url's with just the year, but in years when the
#presidency changes hands, it adds the president's name as well

#skip_list is a list of the years when the presidency changed hands
#skipped_list is a list of what will go in place of the year in the url

skip_list = [1945, 1953, 1961, 1963, 1969, 1974, 1977, 1981, 1989, 1993, 2001, 2009]
skipped_list = ["1945-roosevelt", "1945-truman", "1953-truman", "1953-eisenhower", "1961-eisenhower", "1961-kennedy", "1963-kennedy", "1963-johnson", "1969-johnson", "1969-nixon", "1974-nixon", "1974-ford", "1977-ford", "1977-carter", "1981-carter", "1981-reagan", "1989-reagan", "1989-bush", "1993-bush", "1993-clinton", "2001-clinton", "2001-wbush", "2009-wbush", "2009-obama"]
skip_index = 0	#starting index (for skipped list)

#list of inaugural dates
inaugurations = [datetime.date(1933, 3, 4), datetime.date(1945, 4, 12), datetime.date(1953, 1, 20), datetime.date(1961, 1, 20), datetime.date(1963, 11, 22), datetime.date(1969, 1, 20), datetime.date(1974, 8, 9), datetime.date(1977, 1, 20), datetime.date(1981, 1, 20), datetime.date(1989, 1, 20), datetime.date(1993, 1, 20), datetime.date(2001, 1, 20), datetime.date(2009, 1, 20)]
i_index = 0

#loop through years from 1937 through 2016
while (year < 2017):
	#initalize bool to check for years to skip
	skip_year = False
	#check if year should be skipped
	for skip in skip_list:
		if (year == skip):
			skip_year = True

	#non-skip year
	if (skip_year == False):
		#pass year, file, inaugural date, and exec order count
		extractor(str(year), file, inaugurations[i_index], count)

	#skip year
	else:
		#pass "year-president" string, file, inaugural date
		#and exec order count
		extractor(skipped_list[skip_index], file, inaugurations[i_index], count)
		#increment index for skipped list
		skip_index = skip_index + 1

		#switch presidents

		#open new file with "year-president" string in filename
		file = csv.writer(open(skipped_list[skip_index] + "_orders.csv", "w"))
		#increment index for new inaugural date
		i_index = i_index + 1
		#reset exec order count
		count = 1

		#I could've made this a separate function or something as this
		#code is repeated but it seemed like a waste for only two lines
		extractor(skipped_list[skip_index], file, inaugurations[i_index], count)
		skip_index = skip_index + 1

	#increment year
	year = year + 1

