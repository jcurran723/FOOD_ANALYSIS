import urllib.request, urllib.parse, urllib.error
import json
import sqlite3

# Parts of the url for mining nutrient data:
base_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
api_text = "?api_key="
query_txt = "&query="

# Create a database if it does not already exist
conn = sqlite3.connect('food_db.sqlite')
cur = conn.cursor()

# Create a table in the database with needed parameters
cur.execute('''
            CREATE TABLE IF NOT EXISTS Nutrients(
            foodName TEXT, 
            Protein FLOAT,
            Fat FLOAT,
            Carbs FLOAT,
            Sugars FLOAT,
            Fiber FLOAT,
            NetCarbs FLOAT)
            ''')

# Use "DEMO_KEY" as the api_key unless creating an account, this has limited access.
api_key = "DEMO_KEY"

# Ask for a json file that contains foods to search for
fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'foods.json'
fh = open(fname)

try:
    js = json.load(fh)
except:
    js = None

if not js:
    print("==== Failure To Retreive ====")
    print(js)


searchTerms = []
foodCount = 0

for foods in js["foods"]:

    # Extract the food name and search text from the json file
    foodName = foods["name"]
    searchText = foods["search_text"]
    searchTerms = searchText.split()

    # Check if the food is already in the database, skip if it is
    cur.execute('SELECT foodName FROM Nutrients WHERE foodName=?', (foodName, ))

    try:
        data = cur.fetchone()[0]
        print("Found in database", foodName)
        continue
    except:
        pass

        # The remainder of the code at this level is skipped
        # if the current food in the json file is already
        # in the database.

        print('@@@@@@@@@@@@@@@@@@@ NEW FOOD @@@@@@@@@@@@@@@@@@@')
        print()
        print("Name of food:", foodName)

        # Create the unique url for the selected food not in the database
        # Make a duplicated copy to hide my personal api key.
        # The url is the form of:
        #   https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query=
        #   Followed by the search terms seperated by %20 if necessary.
        # 
        # Example to search for 'Peanut Butter':
        # https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query=Peanut%20Butter
        #
        # Example to search for 'Egg omelet or scrambled egg, made with butter':
        # https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query=Egg%20omelet%20or%20scrambled%20egg,%20made%20with%20butter

        url = base_url + api_text + api_key + query_txt

        for term in searchTerms:
            url = url + term + "%20"
        # Remove last "%20" from url:
        url = url[:len(url)-3]

        print("Retreving", hide_my_key_url)
        urlHandler = urllib.request.urlopen(url)
        data = urlHandler.read().decode()
        print("Retrieved", len(data), "characaters")

        try:
            js = json.loads(data)
        except:
            js = None

        if not js:
            print("==== Failure To Retreive ====")
            print(data)

        #print(json.dumps(js, indent=4))

        food_desciption = js["foods"][0]["description"]

        print()
        print('==========================')
        print(food_desciption)
        print('==========================')
        print()    

        # Initialize each nutrient to 'None' so that if it
        # is not found the program prints that to the screen
        # and assumes a value of zero.
        Protein = None
        Fat = None
        Carbs = None
        Sugars = None
        Fiber = None
        # The net carbs is calculated from Carbs - Fiber
        NetCarbs = 0

        # The json for each food can have many many entries.
        # For example searching 'eggs' gets everything with egg
        # including candy eggs. The search terms used in the
        # json file I created were used to find the appropriate
        # food in the first json entry, so that is why index 0 is
        # used. Each nutrient has a unique number common to all
        # foods which are in the comments below.
        for nutrients in js["foods"][0]["foodNutrients"]:

            # Protein = 203
            if (nutrients["nutrientNumber"] == "203"):
                name = nutrients["nutrientName"]
                units = nutrients["unitName"]
                value = nutrients["value"]
                print("Nutrient:", name)
                print("Units:", units)
                print("Amount:", value)
                print()
                Protein = value

            # Fat = 204
            if (nutrients["nutrientNumber"] == "204"):
                name = nutrients["nutrientName"]
                units = nutrients["unitName"]
                value = nutrients["value"]
                print("Nutrient:", name)
                print("Units:", units)
                print("Amount:", value)
                print()
                Fat = value

            # Carbs = 205
            if (nutrients["nutrientNumber"] == "205"):
                name = nutrients["nutrientName"]
                units = nutrients["unitName"]
                value = nutrients["value"]
                print("Nutrient:", name)
                print("Units:", units)
                print("Amount:", value)
                print()
                Carbs = value

            # Sugars = 269
            if (nutrients["nutrientNumber"] == "269"):
                name = nutrients["nutrientName"]
                units = nutrients["unitName"]
                value = nutrients["value"]
                print("Nutrient:", name)
                print("Units:", units)
                print("Amount:", value)
                print()
                Sugars = value

            # Fiber = 291
            if (nutrients["nutrientNumber"] == "291"):
                name = nutrients["nutrientName"]
                units = nutrients["unitName"]
                value = nutrients["value"]
                print("Nutrient:", name)
                print("Units:", units)
                print("Amount:", value)
                print()
                Fiber = value

        if Protein is None:
            print("Protein was not found, assuming 0.")
            Protein = 0

        if Fat is None:
            print("Fat was not found, assuming 0.")
            Fat = 0

        if Carbs is None:
            print("Carbs was not found, assuming 0.")
            Carbs = 0

        if Sugars is None:
            print("Sugars was not found, assuming 0.")
            Sugars = 0

        if Fiber is None:
            print("Fiber was not found, assuming 0.")
            Fiber = 0

        NetCarbs = Carbs - Fiber
        if NetCarbs < 0:
            NetCarbs = 0

        foodCount = foodCount + 1

        print("Nutrients Summary:")
        print("------------------")
        print("Protein:", Protein)
        print("Fat:", Fat)
        print("Carbs:", Carbs)
        print("Sugars:", Sugars)
        print("Fiber:", Fiber)
        print("NetCarbs:", NetCarbs)
        print()

        # Write the nutrients for the current food into the databse
        cur.execute('''INSERT INTO Nutrients (
                    foodName,
                    Protein,
                    Fat,
                    Carbs,
                    Sugars,        
                    Fiber,
                    NetCarbs        
                    )
                VALUES ( ?, ?, ?, ?, ?, ?, ? )''', (foodName, Protein, Fat, Carbs, Sugars, Fiber, NetCarbs ) )
        conn.commit()

# The end of the food search is donem print the number
# of foods found during this iteration of the program.
print()
print("Retreived data on", foodCount, "foods.")
print()
print("Run graphfoods.py to create bar graph web pages of the mined data.")

cur.close()
