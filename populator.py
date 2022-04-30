from flask import request
import mysql.connector
import requests
from bs4 import BeautifulSoup

# Since mr mime and mime junior have a space in their name, this function is needed
def mime_checker(name):
    if name == "mime-jr":
        name = "Mime Jr."
    elif name == "mr-mime":
        name = "Mr. Mime"
    return name

# db connection object
db = mysql.connector.connect(
    host="crimson.crjdaartjksp.us-east-1.rds.amazonaws.com",
    username="braden",
    password="braden",
    database="project"
)

#cursor object for executing queries
cursor = db.cursor()

# Url for pokemondb.net's list of all moves 
url = "https://pokemondb.net/move/all"

# gets html data from url above
page = requests.get(url)

# Beautiful soup web scraper object | page.content is the raw html and "html.parser" tells the object how process the data (page.content)
soup = BeautifulSoup(page.content, "html.parser")


# Goto "https://pokemondb.net/move/all" to follow along
# 1. Inspect the page and find which html elements you need to scrape.
# 2. In this case: the html element containing all the moves is a table with id='moves'
# 3. Lets grab this table with our soup object.

table = soup.find('table', id='moves')

# 4. Now lets get each table entry

entries = table.find_all('tr')
# print(len(entries))
# > 866

# 5. Now lets grab each specific element of the move for the DB: 
# I am not including any optional elements
# moveName, movePP, movePriority, typeID, moveID (Auto Increment)

# 6. Iterate
# Hardcoding moves without type cuz im too lazy
null_types = ['Dire Claw', 'Esper Wing', 'Headlong Rush', 'Lunar Blessing', 'Mystical Power', 'Take Heart', 'Victory Dance']

for i in range(1, len(entries)):
    move = entries[i]

    moveName = move.find("td", class_='cell-name').text

    # if move doesnt have type, go to next
    if moveName in null_types:
        print("No type")
        continue

    movePP = move.find_all('td', class_="cell-num")[2].string
    if movePP is None:
        movePP = 0

    # there is no data on movePriority in the DB so we will drop from DB


    type = move.find('td', class_="cell-icon").text


    # for type, we need to grab the ID in the types table
    id_query = "SELECT typeID FROM types WHERE type=%s"
    val = (type,)
    cursor.execute(id_query, val)
    # get type id for reference into table
    typeID = int(cursor.fetchall()[0][0])


    # now lets write the actual query to enter the move into the DB

    query = "INSERT INTO moves (moveName, movePP, typeID) VALUES (%s, %s, %s)"
    vals = (moveName, movePP, typeID)

    # run query and commit to DB
    cursor.execute(query, vals)
    db.commit()

    #confirmation message
    print(f"Successfully added move: {moveName} to DB!")
    