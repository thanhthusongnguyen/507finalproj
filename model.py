################################################################################
######################### ---------- INFO ---------- ###########################
################################################################################

### --- FINAL PROJECT FOR SI 507 // WINTER 2018 --------------------------------

## MODEL:
## Total: 1 Global Variable, 1 Class, 8 Functions
## Aggregation of Data: get_wiki, get_shelters, get_records
## Plotting/Displaying Data: plot_shelters, plot_records, DisplayRecord
## Search Specific: breeds_list, get_search_results, search_records


################################################################################
######################### ---------- SETUP ---------- ##########################
################################################################################

### --- IMPORTING MODULES ------------------------------------------------------
import sqlite3

from flask import Flask, render_template
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls


### --- IMPORTING OTHER FILES --------------------------------------------------
import secrets



################################################################################
#################### ---------- DATA PROCESSING ---------- #####################
################################################################################

### --- GLOBAL SEARCH RESULTS --------------------------------------------------
search_results = []


### --- CLASS INSTANCE ---------------------------------------------------------
class DisplayRecord():
	def __init__(self, name, id, primarybreed, secondarybreed, age, sex, location, description):
		self.name = name
		self.id = id
		self.primarybreed = primarybreed
		self.secondarybreed = secondarybreed
		self.age =age
		self.sex = sex
		self.location = location
		self.description = description

	def __str__(self):
		info = "Hello! My name is {} (ID: {}) and I'm a {} {} {}. I currently am living at {}.".format(self.name, self.id, self.age, self.sex, self.primarybreed, self.location)
		return info


### --- DISPLAY WIKIPEDIA BREED INFO -------------------------------------------
def get_wiki(range):
	span = range.split()

	## Connect to Database
	DBNAME = "adoptable_dogs.db"
	try:
		conn = sqlite3.connect(DBNAME)

	except Error as e:
		print(e)

	cur = conn.cursor()

	## Grab Wiki Data
	stmt = """
		SELECT *
		FROM wiki_breeds
		WHERE wiki_breeds_id >= {}
		AND wiki_breeds_id <= {}
	""".format(int(span[0]), int(span[1]))

	cur.execute(stmt)


	## Return List
	wiki_list = []

	for each in cur:
		wiki_list.append(each)


	## Close Database Connection
	conn.commit()
	conn.close()

	return wiki_list


### --- SHELTER INFO -----------------------------------------------------------
def get_shelters(sortby = "name", sortorder = "asc"):

	## Connect to Database
	DBNAME = "adoptable_dogs.db"
	try:
		conn = sqlite3.connect(DBNAME)

	except Error as e:
		print(e)

	cur = conn.cursor()

	## Grab Shelter Data
	stmt = """
		SELECT S.name, C.name, St.name, S.zipcode, S.latitude, S.longitude
		FROM shelter AS S
		JOIN city AS C
			ON S.city = C.city_id
		JOIN state AS St
			ON S.state = ST.state_id	
	"""

	cur.execute(stmt)


	## Return List
	shelter_list = []

	for each in cur:
		shelter_list.append(each)


	## Sort By/Order
	if sortby == "name":
		sortcol = 0

	elif sortby == "city":
		sortcol = 1

	elif sortby == "state":
		sortcol = 2

	elif sortby == "zipcode":
		sortcol = 4

	else:
		sortcol = 0

	rev = (sortorder == 'desc')

	sorted_list = sorted(shelter_list, key = lambda row: row[sortcol], reverse = rev)

	## Close Database Connection
	conn.commit()
	conn.close()

	return sorted_list


### --- MAP SHELTER INFO -------------------------------------------------------

def plot_shelters():
	
	shelter_list = get_shelters()

	## Grabbing Values
	lat_values = []
	lon_values = []
	text_values = []

	for each in shelter_list:
		lat_values.append(each[4])
		lon_values.append(each[5])
		text_values.append(each[0])


	## Creating Trace
	trace0 = dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = lon_values,
		lat = lat_values,
		text = text_values,
		mode = 'markers',
		marker = dict(
			size = 15,
			symbol = 'circle',
			color = 'rgb(102, 114, 146)',
			)
		)

	data = [trace0]

	
	## Scaling and Centering Map
	min_lat = 10000
	max_lat = -10000
	min_lon = 10000
	max_lon = -10000


	### --- Redefining the Boundary Lines --- ###
	for each in lat_values:
		every = float(each)

		if every < min_lat:
			min_lat = every

		if every > max_lat:
			max_lat = every

	for each in lon_values:
		every = float(each)

		if every < min_lon:
			min_lon = every

		if every > max_lon:
			max_lon = every

	center_lat = (max_lat + min_lat) / 2
	center_lon = (max_lon + min_lon) / 2

	max_range = max(abs(max_lat - min_lat), abs(max_lon - min_lon))
	padding = max_range * .10
	
	lat_axis = [min_lat - padding, max_lat + padding]
	lon_axis = [min_lon - padding, max_lon + padding]


	## Title
	title = "Animal Shelters & Rescue Organizations Near Ann Arbor, MI"


	## Layout
	layout = dict(
		geo = dict(
			scope = 'usa',
			projection = dict(type = 'albers usa'),
			showland = True,
			landcolor = "rgb(241, 227, 221)",
			subunitcolor = "rgb(141, 157, 182)",
			countrycolor = "rgb(188, 202, 214)",
			lataxis = {'range': lat_axis},
			lonaxis = {'range': lon_axis},
			center = {'lat': center_lat, 'lon': center_lon},
			countrywidth = 3,
			subunitwidth = 3
			)
		)

	## Plotting Map 
	fig = dict(data = data, layout = layout)
	py.plot(fig, validate = False, filename = title)

	## Embed URL
	# print(tls.get_embed('https://plot.ly/~thanhthusongnguyen/32'))

	return None


### --- GET DOG RECORDS --------------------------------------------------------
def get_records():
	## Connect to Database
	DBNAME = "adoptable_dogs.db"
	try:
		conn = sqlite3.connect(DBNAME)

	except Error as e:
		print(e)

	cur = conn.cursor()


	## Grab Records Data

	## Primary and Secondary Breeds
	stmt = """
		SELECT R.name, R.id, P.name, A.name, Se.name, Sh.name, R.description, P2.name
		FROM records AS R
		JOIN pf_breeds AS P
			ON R.primarybreed = P.pf_breeds_id
		JOIN pf_breeds AS P2
			ON R.secondarybreed = P2.pf_breeds_id
		JOIN age as A
			ON R.age = A.age_id
		JOIN sex AS Se
			ON R.sex = Se.sex_id
		JOIN size AS Si
			ON R.size = Si.size_id
		JOIN shelter AS Sh
			ON R.shelterId = Sh.shelter_id
	"""

	cur.execute(stmt)

	records_list = []

	for each in cur:
		records_list.append(each)


	## Primary Breeds Only
	stmt = """
		SELECT R.name, R.id, P.name, A.name, Se.name, Sh.name, R.description
		FROM records AS R
		JOIN pf_breeds AS P
			ON R.primarybreed = P.pf_breeds_id
		JOIN age as A
			ON R.age = A.age_id
		JOIN sex AS Se
			ON R.sex = Se.sex_id
		JOIN size AS Si
			ON R.size = Si.size_id
		JOIN shelter AS Sh
			ON R.shelterId = Sh.shelter_id
	"""

	cur.execute(stmt)

	for each in cur:
		secondarybreed = (None,)
		each += secondarybreed
		records_list.append(each)


	## Remove Duplicates
	cleaned_records = []
	list_ids = []

	for each in records_list:
		if each[1] not in list_ids:
			list_ids.append(each[1])
			cleaned_records.append(each)


	## Close Database Connection
	conn.commit()
	conn.close()
	
	return cleaned_records


### --- MAP DOG RECORDS --------------------------------------------------------
def plot_records():
	records_list = get_records()

	labels = []
	values = []
	title = "Breakdown of Adoptable Dog Breeds"

	breeds_dict = {}

	for each in records_list:

		if each[7] == None:
			if each[2] in breeds_dict:
				breeds_dict[each[2]] += 1
			else:
				breeds_dict[each[2]] = 1
		
		else:
			if each[7] in breeds_dict:
				breeds_dict[each[7]] += 1
			else:
				breeds_dict[each[7]] = 1

	for each in breeds_dict:
		labels.append(each)
		values.append(breeds_dict[each])


	trace = go.Pie(labels = labels, values = values)
	py.plot([trace], filename = title)

	## Embed URL
	# print(tls.get_embed('https://plot.ly/~thanhthusongnguyen/34'))

	return None


### --- DISPLAY DOG RECORDS ----------------------------------------------------

## Get list of breeds to display as option search parameters
def breeds_list():
	breeds = []
	records_list = get_records()

	for each in records_list:
		if each[7] == None:
			if each[2] not in breeds:
				breeds.append(each[2])

		else:
			if each[7] not in breeds:
				breeds.append(each[7])

	breeds_list = sorted(breeds)
	return breeds_list


## Grab search results for display
def get_search_results():
	global search_results
	return search_results


## Processing Records for Display
def search_records(breed):
	global search_results

	records_list = get_records()

	pulled_records = []

	for each in records_list:
		if each[2] == breed:
			pulled_records.append(each)

	record_display = []

	for each in pulled_records:
		single = []
		phrase = DisplayRecord(each[0], each[1], each[2], each[7], each[3], each[4], each[5], each[6])
		single.append(phrase)
		single.append(each[6])
		record_display.append(single)
	
	search_results = record_display