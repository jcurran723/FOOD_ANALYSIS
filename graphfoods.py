import sqlite3

# Creat an html file to link all the individual food graph pages to:
htmlOut = open('foods.html', 'w')
htmlOut.write('<!DOCTYPE html>')
htmlOut.write('\n')
htmlOut.write('<html lang = "en">')
htmlOut.write('\n')
htmlOut.write('<head>')
htmlOut.write('\n')
htmlOut.write('    <meta charset="UTF-8">')
htmlOut.write('\n')
htmlOut.write('    <title>My Foods</title>')
htmlOut.write('\n')
htmlOut.write('</head>')
htmlOut.write('\n\n')
htmlOut.write('<body>')
htmlOut.write('\n')
htmlOut.write('    <main>')
htmlOut.write('\n')
htmlOut.write('        <h1>Links to my food web pages</h1>')
htmlOut.write('\n')
htmlOut.write('        <h2>Click on any link below to show a graph of its nutritional data.</h2>')
htmlOut.write('\n\n')

# Open the food database:
conn = sqlite3.connect('food_db.sqlite')
cur = conn.cursor()
cur.execute('SELECT foodName, Protein, Fat, Carbs, Sugars, Fiber, NetCarbs FROM Nutrients')

# Load all the food data into a dictionary
foodData = dict()
for data_row in cur:      #  Protein      Fat          Carbs        Sugars       Fiber        NetCarbs
    foodData[data_row[0]] = (data_row[1], data_row[2], data_row[3], data_row[4], data_row[5], data_row[6])

# Print out how many foods were retreived from the database and the data:
print()
print("Loaded data on", len(foodData), "foods.")
print()
print(foodData)
print()

# Print out the name and data for each food:
for food in foodData:
    print(food) #Prints the named food
    # For JavaScript and HTML create food name with no spaces
    singleWordName = food.replace(" ", "")
    print("singleWordName:", singleWordName)
    print("Protein:", foodData[food][0])
    print("Fat:", foodData[food][1])
    print("Carbs:", foodData[food][2])
    print("Sugars:", foodData[food][3])
    print("Fiber:", foodData[food][4])
    print("Net Carbs:", foodData[food][5])

    # Create new html file:
    print("Creating the", singleWordName, ".html file.")
    fin = open('blank.html', 'r')
    fout = open(singleWordName+'.html', 'w')
    for line in fin:
        fout.write(line.replace('blank.js', singleWordName+'.js'))
    fin.close()
    fout.close()

    # Create new Java Script File for each food:
    print("Creating the", singleWordName, ".js file.")
    fout = open(singleWordName+'.js', 'w')
    fout.write('myData = ["')
    fout.write(singleWordName)
    fout.write('", ')
    fout.write(str(foodData[food][0])+', ')
    fout.write(str(foodData[food][1])+', ')
    fout.write(str(foodData[food][2])+', ')
    fout.write(str(foodData[food][3])+', ')
    fout.write(str(foodData[food][4])+', ')
    fout.write(str(foodData[food][5]))
    fout.write('];')
    fout.close()

    # Create new Java Script File for each food:
    print("Updating the food.html to link to the", singleWordName, ".html file.")
    htmlOut.write('        <p><a href="'+singleWordName+'.html"target="_blank">'+food+'</a></p>')
    htmlOut.write('\n')

    print()


print("Finish updating the foods.html page.")
htmlOut.write('    </main>')
htmlOut.write('\n')
htmlOut.write('</body>')
htmlOut.write('\n')
htmlOut.write('</html>')
# Close out the foods.html file
htmlOut.close()

# Close the foods_db.sqlite
cur.close()

print()
print("Open the foods.html containing links to bar graphs of nutritional information for each food in your list.")