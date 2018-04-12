################################################################################
######################### ---------- INFO ---------- ###########################
################################################################################

## FINAL PROJECT FOR SI 507 // WINTER 2018


################################################################################
######################### ---------- SETUP ---------- ##########################
################################################################################
import json
import requests
import secrets
from bs4 import BeautifulSoup

from flask import Flask, render_template
import plotly.plotly as py
import webbrowser



################################################################################
######################### ---------- CACHE ---------- ##########################
################################################################################

##### --- SETTING UP CACHE -----------------------------------------------------

CACHE_FNAME = "finalproj_cache.json"

try:
	cache_file = open(CACHE_FNAME, "r")
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

except:
	CACHE_DICTION = {}



################################################################################
###################### ---------- WEB CRAWLING ---------- ######################
################################################################################

##### --- UNIQUE KEY -----------------------------------------------------------

def get_unique_key(url):
	return (url)


##### --- GRABBING DATA FROM DOG BREEDS WIKIPEDIA PAGE -------------------------

def scrape_wiki(url):
	unique_ident = get_unique_key(url)

	if unique_ident in CACHE_DICTION:
		print("Getting cached data...\n")

		return CACHE_DICTION[unique_ident]

	else:
		print("Making a request for new data...\n")

		resp = requests.get(url)
		CACHE_DICTION[unique_ident] = resp.text
		dumped_json_cache = json.dumps(CACHE_DICTION)

		fw = open(CACHE_FNAME, "w")
		fw.write(dumped_json_cache)
		fw.close()

		return CACHE_DICTION[unique_ident]


##### --- WEBSCRAPING DOG BREEDS WIKIPEDIA PAGE --------------------------------

def webscape_wiki(data):
	soup = BeautifulSoup(data, "html.parser")
	table = soup.find_all(class_ = "wikitable")

	list_breeds = []

	for rows in table:
		row = rows.find_all("tr")

		for cell in row:
			data = cell.find("td")

			if 'bs4' in str(type(data)):
				breed = data.strip
				list_breeds.append(breed)
	
			







################################################################################
###################### ---------- RUNNING DATA ---------- ######################
################################################################################

##### --- INITIALIZE -----------------------------------------------------------

if __name__ == '__main__':
	
	## Grabbing Data from Wikipedia
	url = "https://en.wikipedia.org/wiki/List_of_dog_breeds"
	wiki_data = scrape_wiki(url)

	## Webscraping Page
	webscape_wiki(wiki_data)