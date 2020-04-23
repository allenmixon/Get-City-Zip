import requests
import csv
import urllib.parse


#Your address file here
fn = 'mail_list.csv' 

#open file
with open(fn, 'r') as csv_file:

		csv_reader = csv.reader(csv_file)
		column_names = next(csv_reader)

		loc = column_names.index('Address')
	
		with open(('new_' + fn), 'w') as new_file:
			csv_writer = csv.writer(new_file)

			#Add new columns
			column_names.append('Street')
			column_names.append('City-St-Zip')
			csv_writer.writerow(column_names)

			#read and write
			for line in csv_reader:

				#call google maps api
				search = line[loc] + ' MS' #search address and state (your state here)
				encoded_search = urllib.parse.quote(search)
				http_request = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=formatted_address&key=YOUR_KEY_HERE'.format(encoded_search)
				r = requests.get(http_request)
				jdata = r.json()

				#parse string data
				address = (jdata['candidates'][0] if len(jdata['candidates']) >= 1 else '')

				#append new data unless empy just print line
				if address != '':
					street = address['formatted_address'].split(',')[0]
					city_st_zip_co = address['formatted_address'].split(',', 1)[1]
					city_st_zip = city_st_zip_co.rsplit(',',1)[0]

					#add new rows
					line.append(street)
					line.append(city_st_zip)

				#write new rows
				print(address)
				csv_writer.writerow(line)