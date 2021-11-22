README for FOOD_ANALYSIS Python program.

These Python 3 files will read a json file, check if
a food is in the food database named food_db_sqlite
and if not search for it in the online data source. 
The data is retrieved from: https://api.nal.usda.gov.
It then retrieves for each food the following nutrient
values which are all listed as per 100 grams:\

	Protein
	Fat
	Carbs
	Sugars
	Fiber
	Net Carbs are calculated by Carbs - Fiber

The name of the food and all the values above are then stored
into the food_db.sqlite database file. The program is designed
so it can be stopped and restarted at anytime and will leave 
where it left off or start with a different json file.

All of the above is done by first creating a json file. See 
food.json for an example. Then running the getfoods.py program.

NOTE: The getfoods.py software used the 'DEMO_KEY' API KEY which
can be used for a limited time. If you use this more you can sign
up for a free unique API KEY to replace the 'DEMO_KEY' with. See
https://api.nal.usda.gov.

After you have the database updated via running getfoods.py you
can run the other Python program which is called graphfoods.py.

The graphfoods.py software will read the food_db_sqlite database
and then create a html and javascript file for each food in the 
database. It also created a foods.html file that will contain 
links to each individual food html file. All the files together
allow the nutritional information for each food to displayed in
a Google Bar graph web page.
