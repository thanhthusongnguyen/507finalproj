################################################################################
######################### ---------- INFO ---------- ###########################
################################################################################

### --- FINAL PROJECT FOR SI 507 // WINTER 2018 --------------------------------

## Creating "adoptable_dogs" database
## Creating tables in database
## Populating tables in database



################################################################################
######################### ---------- SETUP ---------- ##########################
################################################################################

### --- IMPORTING MODULES ------------------------------------------------------
import sqlite3
import json
import requests
from bs4 import BeautifulSoup


### --- IMPORTING OTHER FILES --------------------------------------------------
import secrets
import get_data



################################################################################
####################### ---------- ADD BREEDS ---------- #######################
################################################################################

DBNAME = 'adoptable_dogs.db'

### --- CREATING DATABASE ------------------------------------------------------
def create_DB():

	## Connect to Database
	try:
		conn = sqlite3.connect(DBNAME)

	except Error as e:
		print(e)

	cur = conn.cursor()


	### --- WIKI BREEDS TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'wiki_breeds';
	"""
	cur.execute(stmt)
	
	## Create Table
	stmt = """
		CREATE TABLE 'wiki_breeds' (
		'wiki_breeds_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT,
		'url' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	### --- STATE TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'state';
	"""
	cur.execute(stmt)

	## Create Table
	stmt = """
		CREATE TABLE 'state' (
		'state_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	### --- CITY TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'city';
	"""
	cur.execute(stmt)

	## Create Table
	stmt = """
		CREATE TABLE 'city' (
		'city_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	### --- SHELTER TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'shelter';
	"""
	cur.execute(stmt)

	## Create Table
	stmt = """
		CREATE TABLE 'shelter' (
		'shelter_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT,
		'id' TEXT,
		'city' INTEGER,
		'state' INTEGER,
		'zipcode' INTEGER,
		'latitude' TEXT,
		'longitude' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	### --- STATUS TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'status';
	"""
	cur.execute(stmt)

	## Create Table
	stmt = """
		CREATE TABLE 'status' (
		'status' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT,
		'code' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	### --- AGE TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'age';
	"""
	cur.execute(stmt)

	## Create Table
	stmt = """
		CREATE TABLE 'age' (
		'age_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	### --- SEX TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'sex';
	"""
	cur.execute(stmt)
	
	## Create Table
	stmt = """
		CREATE TABLE 'sex' (
		'sex_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT,
		'code' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	### --- SIZE TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'size';
	"""
	cur.execute(stmt)

	## Create Table
	stmt = """
		CREATE TABLE 'size' (
		'size_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT,
		'code' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	### --- PF BREEDS TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'pf_breeds';
	"""
	cur.execute(stmt)

	## Create Table
	stmt = """
		CREATE TABLE 'pf_breeds' (
		'pf_breeds_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	### --- PF RECORDS TABLE --- ###
	## Drop Table If Exists
	stmt = """
		DROP TABLE IF EXISTS 'records';
	"""
	cur.execute(stmt)

	## Create Table
	stmt = """
		CREATE TABLE 'records' (
		'records_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'name' TEXT,
		'id' INTEGER,
		'primarybreed' INTEGER,
		'secondarybreed' INTEGER,
		'age' INTEGER,
		'sex' INTEGER,
		'size' INTEGER,
		'status' INTEGER,
		'shelterId' INTEGER,
		'description' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()


	## Close Database Connection
	conn.close()


### --- POPULATING DATABASE ----------------------------------------------------
def populate_DB():

	## CONNECT TO DATABASE

	try:
		conn = sqlite3.connect(DBNAME)

	except Error as e:
		print(e)

	cur = conn.cursor()

	### --- WIKI BREEDS TABLE --- ###

	for each in get_data.wiki_breedslist:
		data = (None, each[0], each[1])
		
		stmt = """
			INSERT INTO wiki_breeds
			VALUES (?, ?, ?)
		"""

		cur.execute(stmt, data)

	conn.commit()


	### --- STATE TABLE --- ###
	state_dict = {}
	num = 1

	## Find States
	states_unsorted = []

	for each in get_data.pf_locations:
		if each[3] != None:
			if each[3] not in states_unsorted:
				states_unsorted.append(each[3])

	states = sorted(states_unsorted)

	## Create Table
	for each in states:
		data = (None, each)

		stmt = """
			INSERT INTO state
			VALUES (?, ?);
		"""

		cur.execute(stmt, data)

		## Create Dictionary
		state_dict[each] = num
		num += 1

	conn.commit()


	### --- CITY TABLE --- ###
	city_dict = {}
	num = 1

	## Find States
	cities_unsorted = []

	for each in get_data.pf_locations:
		if each[2] != None:
			if each[2] not in cities_unsorted:
				cities_unsorted.append(each[2])

	cities = sorted(cities_unsorted)

	# Create Table
	for each in cities:
		data = (None, each)

		stmt = """
			INSERT INTO city
			VALUES (?, ?);
		"""

		cur.execute(stmt, data)

		## Create Dictionary
		city_dict[each] = num
		num += 1

	conn.commit()


	### --- SHELTER TABLE --- ###
	shelter_dict = {}
	num = 1

	# Create Table
	pf_locations = (get_data.pf_locations)
	for each in pf_locations:
		data = ()

		if each[0] != None:
			data = (None, each[0], each[1], city_dict[each[2]], state_dict[each[3]], each[4], each[5], each[6])
		
		else:
			data = (None, None, each[1], None, None, None, None, None)

		stmt = """
			INSERT INTO shelter
			VALUES (?, ?, ?, ?, ?, ?, ?, ?);
		"""

		cur.execute(stmt, data)

		## Create Dictionary
		shelter_dict[each[1]] = num
		num += 1

	conn.commit()


	### --- STATUS TABLE --- ###
	status_dict = {}
	num = 1
	status = (("Adoptable", "A"), ("Hold", "H"), ("Pending", "P"), ("Adopted", "X"))

	for each in status:
		data = (None, each[0], each[1])

		stmt = """
			INSERT INTO status
			VALUES(?, ?, ?);
		"""
		cur.execute(stmt, data)

		## Create Dictionary
		status_dict[each[1]] = num
		num += 1

	conn.commit()

	### --- AGE TABLE --- ###
	age_dict = {}
	num = 1
	age = ("Baby", "Young", "Adult", "Senior")
	
	## Create Table
	for each in age:
		data = (None, each)

		stmt = """
			INSERT INTO age
			VALUES(?, ?);
		"""
		cur.execute(stmt, data)

		## Create Dictionary
		age_dict[each] = num
		num += 1

	conn.commit()


	### --- SEX TABLE --- ###
	sex_dict = {}
	num = 1
	sex = (("Male", "M"), ("Female", "F"))

	## Create Table
	for each in sex:
		data = (None, each[0], each[1])
		
		stmt = """
			INSERT INTO sex
			VALUES(?, ?, ?);
		"""
		cur.execute(stmt, data)

		## Create Dictionary
		sex_dict[each[1]] = num
		num += 1

	conn.commit()


	### --- SIZE TABLE --- ###
	size_dict = {}
	num = 1
	size = (("Small", "S"), ("Medium", "M"), ("Large", "L"), ("Extra-Large", "XL"))

	## Create Table
	for each in size:
		data = (None, each[0], each[1])

		stmt = """
			INSERT INTO size
			VALUES (?, ?, ?);
		"""
		cur.execute(stmt, data)

		## Create Dictionary
		size_dict[each[1]] = num
		num += 1

	conn.commit()


	### --- PF BREEDS TABLE --- ###
	pf_breeds_dict = {}
	num = 1

	## Create Table
	for each in get_data.pf_breedslist:
		data = (None, each)

		stmt = """
			INSERT INTO pf_breeds
			VALUES (?, ?);
		"""
		cur.execute(stmt, data)

		## Create Dictionary
		pf_breeds_dict[each] = num
		num += 1

	conn.commit()


	### --- Records TABLE --- ###
	## Create Table
	for each in get_data.pf_records:
		data = ()
		if each[3] != None:
			data = (None, each[0], each[1], pf_breeds_dict[each[2]], pf_breeds_dict[each[3]], age_dict[each[4]], sex_dict[each[5]], size_dict[each[6]], status_dict[each[7]], shelter_dict[each[8]], each[9])
		else:
			data = (None, each[0], each[1], pf_breeds_dict[each[2]], None, age_dict[each[4]], sex_dict[each[5]], size_dict[each[6]], status_dict[each[7]], shelter_dict[each[8]], each[9])

		stmt = """
			INSERT INTO records
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
		"""
		cur.execute(stmt, data)

	conn.commit()


	## Close Database Connection
	conn.close()


################################################################################
###################### ---------- RUNNING DATA ---------- ######################
################################################################################
	
## Create Database
create_DB()

## Populate Database
populate_DB()