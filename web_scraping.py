import requests
from bs4 import BeautifulSoup
import csv
cities_data = [] #dictionary used to save details about city

#Function used to extract data out of table present in the link
def extracting(link):
	try:
		page = requests.get(link)
		soup = BeautifulSoup(page.content,'html.parser')
		soup.prettify()
		selected_table = []
		all_tables = soup.find_all('table')
		if len(all_tables)==2:
			selected_table = all_tables[1]
		elif len(all_tables)==1:
			rowcount = len(all_tables[0].find_all('tr'))
			if rowcount > 1:
				selected_table = all_tables[0]
		if len(selected_table)==0:
			print ("No table")
		else:
			cnt = 0
			for row in selected_table.find_all("tr")[1:]:
				city_data = BeautifulSoup(str(row), 'html.parser')
				data_list = city_data.find_all('td')
				with open("data.csv", "a") as csvfile:
        			csvwriter = csv.writer(csvfile,  delimiter=',')
        			csvwriter.writerow([data_list[0].text, data_list[2].text, data_list[4].text, data_list[5].text, data_list[6].text, data_list[7].text])
        			print ("Points written sucessfully to file")
	except:
		print ("Page Unresponsive....")

links = [] #To store all the links that contain information in form of end tables

#Function to find the links of webpages containing data in form of tables
def findlinks(link):
	#print link
	try:
		wiki = "http://www.fallingrain.com"
		page = requests.get(link)
		soup = BeautifulSoup(page.content,'html.parser')
		all_tables = soup.find_all('table')
		if len(all_tables)==2:
			print (link)
			links.append(link)
			return
		elif len(all_tables)==1:
			rowcount = len(all_tables[0].find_all('tr'))
			if rowcount > 1:
				print (link)
				links.append(link)
				return
			else:
				all_links = soup.find_all("a")
				for link in all_links:
		 			temp = link.get("href")
		 			if temp[0]=='/':
		 				temp = wiki + temp
		 				#print temp
		 				findlinks(temp)
		 				#print "here"	
		else:
			all_links = soup.find_all("a")
			for link in all_links:
		 		temp = link.get("href")
		 		if temp[0]=='/':
		 			temp = wiki + temp
		 			#print temp
		 			findlinks(temp)
		 			#print "here"
		

	except: 
		print ("Page Unresponsive....")

link = "http://www.fallingrain.com/world/IN/"
response = requests.get(link)
page = BeautifulSoup(response.text, 'html.parser')
span_data = page.findAll('li')
state_index = []
for state in span_data:
    page = BeautifulSoup(str(state), 'html.parser')
    state_index.append(page.find_all('a')[0]['href'][10:12])

for index in state_index:
    findlinks('http://www.fallingrain.com/world/IN/' + index)
# print (links)

for linking in links:
	extracting(linking)

with open('data.csv', 'w') as csvfile:
    fieldnames = ['Name', 'State', 'latitude',
                  'Longitude', 'Elevation', 'Population']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in cities_data:
        writer.writerow(row)
