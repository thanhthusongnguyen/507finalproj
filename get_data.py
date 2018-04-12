################################################################################
######################### ---------- INFO ---------- ###########################
################################################################################

### --- FINAL PROJECT FOR SI 507 // WINTER 2018 --------------------------------

## Webscraping from "List of Dog Breeds" page on Wikipedia
## Grabbing Data from PetFinder API



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
				breed = data.text
				list_breeds.append(breed)


	return list_breeds



################################################################################
##################### ---------- PETFINDER DATA ---------- #####################
################################################################################

##### --- PETFINDER API KEY & SECRET -------------------------------------------

API_KEY = secrets.API_KEY
API_SECRET = secrets.API_SECRET


##### --- HELPER FUNCTION ------------------------------------------------------

def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
	alphabetized_keys = sorted(params_d.keys())
	res = []

	for k in alphabetized_keys:
	
		if k not in private_keys:
			res.append("{}-{}".format(k, params_d[k]))
	
	return baseurl + "_".join(res)


##### --- PETFINDER API SEARCH -------------------------------------------------

# def get_PF_data(terms):

# 	baseurl = "http://api.petfinder.com/pet.find"
# 	params_diction = {}
# 	params_diction["key"] = API_KEY
# 	params_diction["format"] = "json"
# 	params_diction["output"] = "full"

def get_breeds():
	baseurl = "http://api.petfinder.com/breed.list"
	params_diction = {}
	params_diction["key"] = API_KEY
	params_diction["format"] = "json"
	params_diction["animal"] = "dog"

	unique_ident = params_unique_combination(baseurl, params_diction)

	if unique_ident in CACHE_DICTION:
		print("Getting data from cache...\n")
		PF_breeds_data = CACHE_DICTION[unique_ident]
		return PF_breeds_data

	else:
		print("Making request to API...\n")
		PF_breeds_resp = requests.get(baseurl, params = params_diction)
		PF_breeds_text = PF_breeds_resp.text
		CACHE_DICTION[unique_ident] = json.loads(PF_breeds_text)
		dumped_json_cache = json.dumps(CACHE_DICTION, sort_keys = True, indent = 2)
		fw = open(CACHE_FNAME, "w")
		fw.write(dumped_json_cache)
		fw.close()
		PF_breeds_data = CACHE_DICTION[unique_ident]
		return PF_breeds_data



################################################################################
###################### ---------- RUNNING DATA ---------- ######################
################################################################################
	
## Grabbing Data from Wikipedia
# url = "https://en.wikipedia.org/wiki/List_of_dog_breeds"
# wiki_data = scrape_wiki(url)

## Webscraping Page
# breeds_list = webscape_wiki(wiki_data)

## Petfinder Breeds List
PF_list = get_breeds()

breeds_list = PF_list["petfinder"]["breeds"]["breed"]

for each in breeds_list:
	print(each['$t'])