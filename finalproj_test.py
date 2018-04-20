###########################################################################################
############################## ---------- INFO ---------- ################################
##########################################################################################

### --- FINAL PROJECT FOR SI 507 // WINTER 2018 ------------------------------------------

## UNITTESTING:
## Total: 5 Different Routes
## Display Pages: Index, Rescue, Rescue Map, Breeds Chart, Adoptable Dogs
## POST Route: Search Breeds



##########################################################################################
############################## ---------- SETUP ---------- ###############################
##########################################################################################

### --- IMPORTING MODULES ----------------------------------------------------------------
import unittest


### --- IMPORTING OTHER FILES ------------------------------------------------------------
from get_data import *
import secrets
from add_data import *
from model import *



##########################################################################################
############################ ---------- UNITTESTS ---------- #############################
##########################################################################################

### --- TESTING DATA ACCESS --------------------------------------------------------------

class TestDatabase(unittest.TestCase):

	## TESTING ONE TO ONE TABLES
	def test_one_tables(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		stmt = """
			SELECT name
			FROM wiki_breeds
		"""
		results = cur.execute(stmt)
		results_list = results.fetchall()

		self.assertEqual(len(results_list), 514)
		self.assertIn(('Dachshund',), results_list)

		stmt = """
			SELECT *
			FROM size
		"""

		results = cur.execute(stmt)
		results_list = results.fetchall()
		
		self.assertEqual(len(results_list), 4)
		self.assertIn((4, 'Extra-Large', 'XL'), results_list)

		conn.close()


	## TESTING ONE TO MANY TABLES (SHELTERS)
	def test_joins_shelter(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		stmt = """
			SELECT S.name, C.name, St.name
			FROM shelter AS S
			JOIN city AS C
				ON S.city = C.city_id
			JOIN state AS St
				ON S.state = St.state_id
			WHERE C.name = "Ann Arbor"
			ORDER BY S.name ASC
		"""

		results = cur.execute(stmt)
		results_list = results.fetchall()
		
		self.assertEqual(len(results_list), 7)
		self.assertEqual(results_list[2][0], 'Humane Society of Huron Valley')

		stmt = """
			SELECT C.name, COUNT(S.city)
			FROM shelter AS S
			JOIN city AS C
				ON S.city = C.city_id
			JOIN state AS St
				ON S.state = St.state_id
			WHERE St.name = "MI"
			GROUP BY S.city
			ORDER BY S.city ASC
		"""

		results = cur.execute(stmt)
		results_list = results.fetchall()
		
		self.assertEqual(len(results_list), 59)
		self.assertEqual(results_list[27][1], 8)

		conn.close()


	## TESTING ONE TO MANY TABLES (DOG RECORDS)
	def test_joins_records(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

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
		ORDER BY P.name DESC
		"""

		results = cur.execute(stmt)
		results_list = results.fetchall()

		self.assertEqual(len(results_list), 77)
		self.assertEqual(results_list[0][2], 'Yorkshire Terrier Yorkie')

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
			WHERE A.name = "Young"
			ORDER BY R.name ASC
		"""

		results = cur.execute(stmt)
		results_list = results.fetchall()

		self.assertEqual(len(results_list), 35)
		self.assertEqual(results_list[30][0], 'Sam')

		conn.close()



### --- TESTING CLASS --------------------------------------------------------------------

class TestDisplayRecord(unittest.TestCase):

	def test_DisplayRecord(self):
		record1 = DisplayRecord('Paisley', '123456', 'Australian Cattle Dog', 'Terrier', 'Young', 'Female', 'Humane Society of Huron Valley', "I'm fun; who doesn't love fun?")

		record2 = DisplayRecord('Molly', '123456', 'Poodle', 'Golden Retreiver', 'Adult', 'Female', 'BC SPCA', "I'm itchy.")

		self.assertEqual(str(record1), "Hello! My name is Paisley (ID: 123456) and I'm a Young Female Australian Cattle Dog. I currently am living at Humane Society of Huron Valley.")
		self.assertEqual(str(record2), "Hello! My name is Molly (ID: 123456) and I'm a Adult Female Poodle. I currently am living at BC SPCA.")



### --- TESTING PLOTS --------------------------------------------------------------------

class TestPlotting(unittest.TestCase):
	
	## Mapping Shelters
	def test_plot_shelters(self):
		try:
			plot_shelters()

		except:
			self.fail()


	## Graphing Dog Breeds
	def test_plot_records(self):
		try:
			plot_records()

		except:
			self.fail()




##########################################################################################
########################## ---------- RUNNING CODE ---------- ############################
##########################################################################################

unittest.main(verbosity = 2)