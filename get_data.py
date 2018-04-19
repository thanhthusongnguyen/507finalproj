################################################################################
######################### ---------- INFO ---------- ###########################
################################################################################

### --- FINAL PROJECT FOR SI 507 // WINTER 2018 --------------------------------

## Webscraping from "List of Dog Breeds" page on Wikipedia
## Grabbing Data from PetFinder API



################################################################################
######################### ---------- SETUP ---------- ##########################
################################################################################

### --- IMPORTING MODULES ------------------------------------------------------

import json
import requests
from bs4 import BeautifulSoup


### --- IMPORTING OTHER FILES --------------------------------------------------
import secrets


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
				dog = []
				baseurl = "https://en.wikipedia.org"
				
				breed = data.text
				dog.append(breed)

				link = data.find('a')
				url = link['href']
				fullurl = baseurl + url
				dog.append(fullurl)

				list_breeds.append(dog)

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


##### --- LIST OF DOG BREEDS ON PETFINDER --------------------------------------

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


##### --- LIST OF SHELTERS -----------------------------------------------------

def get_shelters(term):
	baseurl = "http://api.petfinder.com/shelter.find"
	params_diction = {}
	params_diction["key"] = API_KEY
	params_diction["format"] = "json"
	params_diction["location"] = term
	params_diction["count"] = 100

	unique_ident = params_unique_combination(baseurl, params_diction)

	if unique_ident in CACHE_DICTION:
		print("Getting data from cache...\n")
		pf_shelter_data = CACHE_DICTION[unique_ident]
		return pf_shelter_data

	else:
		print("Making request to API...\n")
		pf_shelter_resp = requests.get(baseurl, params = params_diction)
		pf_shelter_text = pf_shelter_resp.text
		CACHE_DICTION[unique_ident] = json.loads(pf_shelter_text)
		dumped_json_cache = json.dumps(CACHE_DICTION, sort_keys = True, indent = 2)
		fw = open(CACHE_FNAME, "w")
		fw.write(dumped_json_cache)
		fw.close()
		pf_shelter_data = CACHE_DICTION[unique_ident]
		return pf_shelter_data


def get_oneshelter(term):
	baseurl = "http://api.petfinder.com/shelter.get"
	params_diction = {}
	params_diction["key"] = API_KEY
	params_diction["format"] = "json"
	params_diction["id"] = term

	unique_ident = params_unique_combination(baseurl, params_diction)

	if unique_ident in CACHE_DICTION:
		print("Getting data from cache...\n")
		pf_oneshelter = CACHE_DICTION[unique_ident]
		return pf_oneshelter

	else:
		print("Making request to API...\n")
		pf_oneshelter_resp = requests.get(baseurl, params = params_diction)
		pf_oneshelter_text = pf_oneshelter_resp.text
		CACHE_DICTION[unique_ident] = json.loads(pf_oneshelter_text)
		dumped_json_cache = json.dumps(CACHE_DICTION, sort_keys = True, indent = 2)
		fw = open(CACHE_FNAME, "w")
		fw.write(dumped_json_cache)
		fw.close()
		pf_oneshelter = CACHE_DICTION[unique_ident]
		return pf_oneshelter


##### --- PULLING 200 DOG RECORDS ----------------------------------------------

def get_PF_data(terms):

	baseurl = "http://api.petfinder.com/pet.find"
	params_diction = {}
	params_diction["key"] = API_KEY
	params_diction["format"] = "json"
	params_diction["output"] = "full"
	params_diction["count"] = 200
	params_diction["animal"] = "dog"
	params_diction["location"] = terms

	unique_ident = params_unique_combination(baseurl, params_diction)

	if unique_ident in CACHE_DICTION:
		print("Getting data from cache...\n")
		pf_data = CACHE_DICTION[unique_ident]
		return pf_data

	else:
		print("Making request to API...\n")
		pf_resp = requests.get(baseurl, params = params_diction)
		pf_text = pf_resp.text
		CACHE_DICTION[unique_ident] = json.loads(pf_text)
		dumped_json_cache = json.dumps(CACHE_DICTION, sort_keys = True, indent = 2)
		fw = open(CACHE_FNAME, "w")
		fw.write(dumped_json_cache)
		fw.close()
		pf_data = CACHE_DICTION[unique_ident]
		return pf_data



################################################################################
###################### ---------- RUNNING DATA ---------- ######################
################################################################################

##### --- GRABBING DATA FROM WIKIPEDIA -----------------------------------------

# Webscraping Page
url = "https://en.wikipedia.org/wiki/List_of_dog_breeds"
wiki_data = scrape_wiki(url)


# Creating Breeds List (Name, URL)
wiki_breedslist = webscape_wiki(wiki_data)


##### --- GRABBING DATA FROM PETFINDER -----------------------------------------

# Petfinder Shelters List (100)
pf_shelters = get_shelters("Ann Arbor, MI")

shelters_raw = pf_shelters["petfinder"]["shelters"]["shelter"]
pf_locations = []

for each in range(100):
	location = []

	name = shelters_raw[each]["name"]["$t"]
	location.append(name)
	
	pf_id = shelters_raw[each]["id"]["$t"]
	location.append(pf_id)

	city = shelters_raw[each]["city"]["$t"]
	location.append(city)

	state = shelters_raw[each]["state"]["$t"]
	location.append(state)

	zipcode = shelters_raw[each]["zip"]["$t"]
	location.append(zipcode)

	latitude = shelters_raw[each]["latitude"]["$t"]
	location.append(latitude)

	longitude = shelters_raw[each]["longitude"]["$t"]
	location.append(longitude)

	if location not in pf_locations:
		pf_locations.append(location)

# Petfinder Shelters Extra
extra_shelters = ["IL74", "LA259", "MA370", "MI1025", "MI232", "MI331", "MI565", "MI579", "OH94", "ON401"]

for each in extra_shelters:
	pf_oneshelter = get_oneshelter(each)
	location = []

	if len(pf_oneshelter["petfinder"]) >= 4:
		oneshelter_raw = pf_oneshelter["petfinder"]["shelter"]

		name = oneshelter_raw["name"]["$t"]
		location.append(name)
		
		pf_id = oneshelter_raw["id"]["$t"]
		location.append(pf_id)

		city = oneshelter_raw["city"]["$t"]
		location.append(city)

		state = oneshelter_raw["state"]["$t"]
		location.append(state)

		zipcode = oneshelter_raw["zip"]["$t"]
		location.append(zipcode)

		latitude = oneshelter_raw["latitude"]["$t"]
		location.append(latitude)

		longitude = oneshelter_raw["longitude"]["$t"]
		location.append(longitude)

	else:
		name = None
		location.append(name)
		
		pf_id = each
		location.append(pf_id)

		city = None
		location.append(city)

		state = None
		location.append(state)

		zipcode = None
		location.append(zipcode)

		latitude = None
		location.append(latitude)

		longitude = None
		location.append(longitude)

	if location not in pf_locations:
		pf_locations.append(location)


# Petfinder Searchable Breeds List
pf_breeds = get_breeds()

breeds_raw = pf_breeds["petfinder"]["breeds"]["breed"]
pf_breedslist = []

for each in breeds_raw:
	pf_breedslist.append(each["$t"])


# Petfinder Records (200)
pf_data = get_PF_data("Ann Arbor, MI")

records_raw = pf_data["petfinder"]["pets"]["pet"]
pf_records = []

for each in range(200):
	record = []

	name = records_raw[each]["name"]["$t"]
	record.append(name)

	pf_id = records_raw[each]["id"]["$t"]
	record.append(pf_id)

	breed = records_raw[each]["breeds"]["breed"]
	if len(breed) == 1:
		primarybreed = breed["$t"]
		record.append(primarybreed)
		record.append(None)

	else:
		primarybreed = breed[0]["$t"]
		record.append(primarybreed)

		secondarybreed = breed[1]["$t"]
		record.append(secondarybreed)

	age = records_raw[each]["age"]["$t"]
	record.append(age)

	sex = records_raw[each]["sex"]["$t"]
	record.append(sex)

	size = records_raw[each]["size"]["$t"]
	record.append(size)

	status = records_raw[each]["status"]["$t"]
	record.append(status)

	shelter_id = records_raw[each]["shelterId"]["$t"]
	record.append(shelter_id)

	description = records_raw[each]["description"]["$t"]
	record.append(description)

	pf_records.append(record)