################################################################################
######################### ---------- INFO ---------- ###########################
################################################################################

### --- FINAL PROJECT FOR SI 507 // WINTER 2018 --------------------------------

## Total: 5 Different Routes
## Display Pages: Index, Rescue, Rescue Map, Breeds Chart, Adoptable Dogs
## POST Route: Search Breeds



################################################################################
######################### ---------- SETUP ---------- ##########################
################################################################################

### --- IMPORTING MODULES ------------------------------------------------------
from flask import Flask, render_template, request, redirect
import plotly.plotly as py
import plotly.graph_objs as go


### --- IMPORTING OTHER FILES --------------------------------------------------
import model



################################################################################
######################### ---------- PAGES ---------- ##########################
################################################################################

app = Flask(__name__)

### --- INDEX ------------------------------------------------------------------
@app.route('/')
def index():
	wiki_data_1 = model.get_wiki("1 257")
	wiki_data_2 = model.get_wiki("258 514")

	return render_template("index.html", wiki_data_1 = wiki_data_1, wiki_data_2 = wiki_data_2)


### --- RESCUE ------------------------------------------------------------------
@app.route('/rescue', methods = ['GET', 'POST'])
def rescue():
	if request.method == "POST":
		sortby = request.form["sortby"]
		sortorder = request.form["sortorder"]
		shelter_list = model.get_shelters(sortby, sortorder)

	else:
		shelter_list = model.get_shelters()

	return render_template("rescue.html", shelter_list = shelter_list)


### --- RESCUE MAP ------------------------------------------------------------------
@app.route('/rescuemap')
def rescuemap():
	return render_template("rescuemap.html")


### --- BREEDS CHART ------------------------------------------------------------------
@app.route('/breedschart')
def breedschart():
	return render_template("breedschart.html")


### --- BREEDS SEARCH ------------------------------------------------------------------
@app.route('/adoptabledogs', methods = ['GET', 'POST'])
def adoptabledogs():
	breeds_list = model.breeds_list()

	return render_template("adoptabledogs.html", breeds_list = breeds_list, search_results = model.get_search_results())


@app.route('/searchbreed', methods = ["POST"])
def searchbreed():
	breed = request.form["breed"]
	model.search_records(breed)

	return redirect('/adoptabledogs')



################################################################################
###################### ---------- RUNNING DATA ---------- ######################
################################################################################
if __name__ == "__main__":
	app.run(debug = True)