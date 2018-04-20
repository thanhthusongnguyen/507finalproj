################################################################################
######################### ---------- INFO ---------- ###########################
################################################################################

### --- FINAL PROJECT FOR SI 507 // WINTER 2018 --------------------------------

## 


################################################################################
######################### ---------- SETUP ---------- ##########################
################################################################################

### --- IMPORTING MODULES ------------------------------------------------------
import sqlite3

import json
import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template
import plotly.plotly as py
import plotly.tools as tls
import webbrowser


### --- IMPORTING OTHER FILES --------------------------------------------------
import secrets



################################################################################
#################### ---------- DATA PROCESSING ---------- #####################
################################################################################

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

	return None



################################################################################
###################### ---------- RUNNING DATA ---------- ######################
################################################################################