################################################################################
######################### ---------- INFO ---------- ###########################
################################################################################

## FINAL PROJECT FOR SI 507 // WINTER 2018

# Populating Tables in Database



################################################################################
######################### ---------- SETUP ---------- ##########################
################################################################################
import sqlite3
import json
import requests
import secrets
from bs4 import BeautifulSoup

from flask import Flask, render_template
import plotly.plotly as py
import webbrowser

import get_data



################################################################################
####################### ---------- ADD BREEDS ---------- #######################
################################################################################

DBNAME = 'adoptable_dogs.db'

def create_DB():

	## CONNECT TO DATABASE

	try:
		conn = sqlite3.connect(DBNAME)

	except Error as e:
		print(e)

	cur = conn.cursor()


	## DROP TABLE IF EXISTS
	stmt = """
		DROP TABLE IF EXISTS 'breeds';
	"""
	cur.execute(stmt)

	
	## CREATE BREEDS TABLE
	stmt = """
		CREATE TABLE 'breeds' (
		'breed_id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'breed' TEXT
		);
	"""
	cur.execute(stmt)
	conn.commit()
	conn.close()


def populate_DB():

	## CONNECT TO DATABASE

	try:
		conn = sqlite3.connect(DBNAME)

	except Error as e:
		print(e)

	cur = conn.cursor()


	## Populate Breeds Table
	for each in get_data.breeds_list:
		data = (None, each)
		
		stmt = """
			INSERT INTO breeds
			VALUES (?, ?)
		"""

		cur.execute(stmt, data)

	conn.commit()
	conn.close()


################################################################################
###################### ---------- RUNNING DATA ---------- ######################
################################################################################

##### --- INITIALIZE -----------------------------------------------------------

# if __name__ == '__main__':
	
	## Create Breeds Database
	# create_DB()
populate_DB()