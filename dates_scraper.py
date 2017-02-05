from bs4 import BeautifulSoup
import urllib2
import csv
import datetime
import datefinder
import re

def extractor( year, f, i_date, count ):
	url_start = "http://www.archives.gov/federal-register/executive-orders/"
	url = url_start + year + ".html"

	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "lxml")
	div = soup.find("div", {"class" : "region region-content"})

	for list in div.findAll("ul"):
		items = list.findAll("li")
		date_signed = items[0].find(text=True)

		#remove periods from date_signed
		date_signed = date_signed.replace(".", "")

		matches = datefinder.find_dates(date_signed)
		for match in matches:
			day_num = abs((match.date() - i_date).days)
			f.writerow([count, day_num])
			count = count + 1

url_start = "http://www.archives.gov/federal-register/executive-orders/"

year = 1937
index = 0
count = 1715

file = csv.writer(open("1937-roosevelt_orders.csv", "w"))

skip_list = [1945, 1953, 1961, 1963, 1969, 1974, 1977, 1981, 1989, 1993, 2001, 2009]
skipped_list = ["1945-roosevelt", "1945-truman", "1953-truman", "1953-eisenhower", "1961-eisenhower", "1961-kennedy", "1963-kennedy", "1963-johnson", "1969-johnson", "1969-nixon", "1974-nixon", "1974-ford", "1977-ford", "1977-carter", "1981-carter", "1981-reagan", "1989-reagan", "1989-bush", "1993-bush", "1993-clinton", "2001-clinton", "2001-wbush", "2009-wbush", "2009-obama"]
inaugurations = [datetime.date(1933, 3, 4), datetime.date(1945, 4, 12), datetime.date(1953, 1, 20), datetime.date(1961, 1, 20), datetime.date(1963, 11, 22), datetime.date(1969, 1, 20), datetime.date(1974, 8, 9), datetime.date(1977, 1, 20), datetime.date(1981, 1, 20), datetime.date(1989, 1, 20), datetime.date(1993, 1, 20), datetime.date(2001, 1, 20), datetime.date(2009, 1, 20)]
i_index = 0

while (year < 2017):
	skip_year = False
	for skip in skip_list:
		if (year == skip):
			skip_year = True
	if (skip_year == False):
		extractor(str(year), file, inaugurations[i_index], count)
	else:
		extractor(skipped_list[index], file, inaugurations[i_index], count)
		index = index + 1

		file = csv.writer(open(skipped_list[index] + "_orders.csv", "w"))
		i_index = i_index + 1
		count = 0

		extractor(skipped_list[index], file, inaugurations[i_index], count)
		index = index + 1
		
	year = year + 1

