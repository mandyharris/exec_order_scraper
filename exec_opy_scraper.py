from bs4 import BeautifulSoup
import urllib3
import csv

wiki = "http://en.wikipedia.org/wiki/List_of_United_States_federal_executive_orders"

#so, if I can find it and it's like wikipedia:
#num = [starting_pres_num]
#url = [most of url]
#ull_end = [list of endings]
#for ending in url_end
	#full_url = url + ending
	#filename = num + "_orders.csv"
	#num = num + 1
http = urllib3.PoolManager()
page = http.request('GET', wiki)
soup = BeautifulSoup(page.data, "lxml")

table = soup.table

f = csv.writer(open("Executive_Orders.csv", "w"))

for row in table.findAll("tr"):
	cells = row.findAll("td") or row.findAll("th")
	pres_num = cells[0].find(text=True)
	name = cells[1].find(text=True)
	total_exo = cells[2].find(text=True)
	years = cells[6].find(text=True)
	f.writerow([pres_num, name, total_exo, years])
