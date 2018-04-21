# SI 507 // Winter 2018 // Final Project

## Synopsis
This is final project for SI 507 in the Winter 2018 semester. It is a showcase of the skills and knowledge I have gained this past semester specifically regarding: accessing data efficiently and responsibily with caching via web scraping and web APIS with authentication, creating and using a database to store and access relational data, basic Python structures, unit tests, data presentation tools, and basic interactivity.

## Data Sources & API Reference
To meet the challenge score of 8, I selected to pull data from two sources: Wikipedia and Petfinder's API

### Wikipedia:
I specifically scraped a Wikipedia page about the different types of dog breeds that exist for their names and for the URLs to their respective Wikipedia pages.

### Petfinder API:
The PetFinder API allows developers access to their database which includes over 300,000 adoptable pets and 11,000 animal welfare organizations. For more information, please visit here (https://www.petfinder.com/developers/api-docs).

#### API Key & Secret
To access the Petfinder API, you need to register for a Petfinder account here (https://www.petfinder.com/developers/api-key) to obtain an API key and secret. Once you have an account and have been assigned an API key and secret, you'll want to create a "secrets.py" file and save both your API key and secret to a respective variable each.

Petfinder does have some restrictions involving their API. You are only allowed 10,000 requests per day, 1,000 records per request, and a maximum of 2,000 records per search.

The Petfinder API has a list of several methods depending on your needs. For the purposes of this project, I utilized the "breed.list" API method (base url: http://api.petfinder.com/breed.list) which returns a list of breeds for a particular animal, the shelter.find method (base url: http://api.petfinder.com/shelter.find) which return a collection of shelter records based on a defined search criteria (in this case, "Ann Arbor, MI"), the shelter.get method (base url: http://api.petfinder.com/shelter.get) which returns a record for a single shelter, and the pet.find method (base url: http://api.petfinder.com/pet.find) which returns pet records according to specified parameters.

## Installations
In order to run the program, I've created you need to install a few modules that aren't already built into Python. All the needed modules to run the program are can be found in the "requirements.txt" file.

### Beautiful Soup
To pull data out of HTML files, please install Beautiful Soup with "pip3 install bs4". For more information about it, you can read more here (https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

### Requests
To make a GET request for our APIs, you'll need the Requests module. To do so, please run "pip3 install requests".

### Flask
To display and present the data through tables and provide interactivity as a website, please install Flask with "pip3 install Flask". For more information about Flask, please visit here ( ttp://flask.pocoo.org/).

### Plotly
This program generates a couple of graph visualizations to present the data. Please install plotly via "pip3 install plotly".

### Sqlite
To create and make requests of the data, you need the Sqlite module and you just add it to the top of your file as "import sqllite3". It would also be potentially beneficial to download the DB Browser for SQL to used a a browser for your created databases.

## Code Structure
As opposed to a single Python file, this code is structured into 6 different files.

### Requesting & Adding Data to Database
Data is collected from Wikipedia using two functions (scrape_wiki(url) and webscrape_wiki(data)). One pulls all the html from the page in question and the other uses Beautiful soup to parse through the html for what I require.

From Petfinder, the functions get_shelters(term) and get_pf_data(term) are used to request data from the Petfinder API. These functions build the url needed to make the request.

After the requests and scraping has been complete, two functions from the "add_data.py" file whill run: create_DB() and populate_DB(). Using a variety of sql statments, a variety of tables (one-to-one and many-to-one) are constructed and populated with the data pulled from Wikipedia and Petfinder.

### Model, View, Controller
Once again, rather than creating a single functioning Python file, I followed the Model, View, Controller pattern.

#### Model:
My "model.py" contains all my data processing functions. For example, contained in here is my class DisplayRecord() which takes a list of aggregated infromation about a dog (name, id number, primary breed, secondary brees, age, sex, location, and description) and returns a string that is to be displayed on the dog records page of my visualization.

#### View:
Using Flask, I have create a total of 5 different html pages which either display information about dogs and breakdown dog breeds of adoptable dogs near Ann Arbor, MI by breed or a table view of the data I have pulled.

#### Controller:
My "app.py" accepts inputs and converts it for commands in either the model or the view. Using html forms for sorting and filter data, I have functions such as def rescue() which allows a user to sort and order shelter information and def adoptabledogs() which pulls dog records from the Petfinder API.

### List & Dictionaries
All of the data I have requested from both data sources is cached in the "finalproj_cache.json" file. It utilizes a dictionary format to store the infromation. I have also used dictionaries when I was building my databases. To ensure that I was insert foreign keys as opposed to nominal values for certain columns of data in my database tables, I would create a dictionary with the nominal term as a key and their primary id as it's value.

Most of the data that I pull from my database are tuples which I think convert to lists for my purposes. I primiarly display the data using lists of information and so to create the HTML tables and PlotLy graphs, many lists were utilized.

## User Guide
As a firm believer in adopting pets from local animal shelters and rescue organization, for my final project, I wanted to create data visualizations that create awareness about dogs who are currently at shelters waiting to be adopted.

Please run the "get_data.py" and "add_data.py" to request and create and populate databases. From there, you can run the "app.py" file while will allow you to open my program in a web browser.

### Home/Index
The home/index page shows you a list of the 514 dog breeds that Wikipedia lists. Each row of data contains a live link to a Wikipedia page with information about that specific breed of dog.

### Shelters
This page presents a table of the lists of shelters near Ann Arbor, MI. You have the option of sorting the information by the shelter's name, city, state, and zipcode. There is also the option of viewing a map plot that I have created in Plotly that plots each shelter's location on a map of the Michigan and it's surroundings states.

### Map
This is a Plotly map of all the shelters listed in the second page of my program.

### Dog Breeds
Next, I present a visualization of the different types of dog breeds that are available for adoption near Ann Arnor, MI.

### Dog Records
From the records in our database, you can enter a breed from the list on the left and pull up information about all the dogs in the database that meet the breed you're searching for. It will display a string of text that includes it's name, Petfinder ID, age, gender, primary breed, and where they're currently located (shelter name) which was generated using my Class.

As you keep entering breed names, the page will refresh to display your most recent search.

## Limitations and Caveats
As the data is constantly being updated (pets get adopted and added to their databases daily), you might have some difficultly running a new search and creating and populating a database. Because of the complicated nature of the how I structured my database tables (with MANY foreign keys referecing a plethora of other tables), incomplete shelter records have thrown a HUGE dent into the functionality of my program as they won't correctly add themselves to my database.

Additionally, with the way the data and program is structures and the way the API method od set up, I can't simply find the shelters that have adoptable dogs and so there is some discrepancy between the list of shelters records and shelter references in the dog records database. It's a work in progress and I am still learning.

Thank you for your time.

